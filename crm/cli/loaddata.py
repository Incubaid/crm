from subprocess import Popen, PIPE
import os

import ujson as json

from sqlalchemy_utils import create_database, database_exists, drop_database

from crm.db import BaseModel, db, RootModel, ManyToManyBaseModel
from crm import app
from crm.user.models import User


@app.cli.command()
def loaddata():
    """
        Load tables with data from filesystem.
    """
    # ensure data dir exists
    from crm import app
    data_dir = app.config["DATA_DIR"]
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        return

    # Keep track of inserted IDs
    # DO NOT check if object exists in DB before insertion to increase performance
    # example: {model_name: [], another_model_name:[]}
    added_object_ids = {}

    # Initialize our dicts
    for model in BaseModel.__subclasses__() + ManyToManyBaseModel.__subclasses__():
        added_object_ids[model.__name__] = []

    # Delete all data in db
    if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        drop_database(app.config['SQLALCHEMY_DATABASE_URI'])

    # create DB
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    # Create tables and run migrations
    p = Popen(['flask', 'db', 'upgrade'], stdout=PIPE, stderr=PIPE)
    p.communicate()[0]

    if p.returncode != 0:
        print('Error in executing command : flask db upgrade .. Make sure migrations dir exists and up2date')
        exit(1)

    # Save users 1st
    model_dir = os.path.abspath(os.path.join(data_dir, User.__name__))

    user_data = {}
    for root, dirs, files in os.walk(model_dir):
        for file in files:
            file_path = os.path.abspath(os.path.join(root, file))
            with open(file_path, 'r') as f:
                data = json.load(f)
                obj = User.from_dict(data)[0]

                if obj.id in added_object_ids[obj.__class__.__name__]:
                    continue

                user_data[obj.id] = {
                    'author_last_id': obj.author_last_id,
                    'author_original_id': obj.author_original_id,
                }

                obj.author_last_id = None
                obj.author_original_id = None
                added_object_ids[obj.__class__.__name__].append(obj.id)
                db.session.add(obj)

    db.session.commit()

    # Now update authors
    for id, info in user_data.items():
        User.query.filter_by(id=id).update(info)
    db.session.commit()

    # START loading
    for model in RootModel.__subclasses__():
        # Root models are 'Company', 'Contact', 'Deal', 'Sprint', 'Project',
        # 'Organization','User'

        model_dir = os.path.abspath(os.path.join(data_dir, model.__name__))
        # many2many objects needed to be added last
        # after all data entered coz they contain references to other models data
        # that may not have been added
        m2m_objects = []
        for root, dirs, files in os.walk(model_dir):
            for file in files:
                file_path = os.path.abspath(os.path.join(root, file))
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    objects = model.from_dict(data)
                    for obj in objects:
                        if hasattr(obj, 'IS_MANY_TO_MANY'):
                            m2m_objects.append(obj)
                            continue
                        if obj.id in added_object_ids[obj.__class__.__name__]:
                            continue
                        added_object_ids[obj.__class__.__name__].append(obj.id)
                        db.session.add(obj)
            db.session.commit()

        m2m_tables = set()
        for obj in m2m_objects:
            m2m_tables.add(obj.__table__.name)
            if obj.id in added_object_ids[obj.__class__.__name__]:
                continue

            db.session.add(obj)
            added_object_ids[obj.__class__.__name__].append(obj.id)
        db.session.commit()

        # we had that nasty bug in loading data
        # since m2m tables has auto-incremental primary keys/idswe load it with old ids
        # but we need our dumped data to be loaded with old Ids
        # By doing so, postgres is not able to detect last ID inserted and causing nasty errors
        # when inserting or updating data that is related to many2many fields
        # we need to reset these tables after insertion and set the next ID to be max(ID) + 1
        for table in m2m_tables:
            db.engine.execute("SELECT setval('%s_id_seq', (SELECT MAX(id) FROM %s)+1);" % (table, table))
