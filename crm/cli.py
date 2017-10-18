import os
from subprocess import Popen, PIPE
import ujson as json

from sqlalchemy_utils import create_database, database_exists, drop_database

from crm.db import BaseModel, db, RootModel, ManyToManyBaseModel
from crm import app

from crm.fixtures import generate_fixtures
from crm.user.models import User


@app.cli.command()
def createdb():
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
    print("DB created.")


@app.cli.command()
def loadfixtures():
    generate_fixtures()


@app.cli.command()
def dumpdata():
    """Dump data table models into filesystem."""
    # ensure database directory

    data_dir = app.config["DATA_DIR"]
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    for model in BaseModel.__subclasses__():
        # Root models are 'Company', 'Contact', 'Deal', 'Sprint', 'Project',
        # 'Organization','User'
        if not model in RootModel.__subclasses__():
            continue

        model_dir = os.path.abspath(os.path.join(data_dir, model.__name__))
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)

        for obj in model.query.all():
            obj_as_str = str(obj).replace('/', '_')
            if len(obj_as_str) > 100:
                obj_as_str = obj_as_str[:100]

            record_path = os.path.abspath(os.path.join(
                model_dir, '%s_%s.json' % (obj.id, obj_as_str)))
            data = obj.as_dict()
            with open(record_path, 'w') as f:
                json.dump(data, f, indent=4)


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

        for obj in m2m_objects:
            if obj.id in added_object_ids[obj.__class__.__name__]:
                continue
            db.session.add(obj)
            added_object_ids[obj.__class__.__name__].append(obj.id)
        db.session.commit()


@app.cli.command()
def generate_graphql_docs():
    """
    Generates schema.graphql IDL file and the GraphQL API documentation for queries and mutations.

    requires graphdoc to be installed.

    """
    from crm import app
    sc = app.graphql_schema
    with open('schema.graphql', "w") as f:
        f.write(str(sc))
    p = Popen(['graphdoc', '-s', './schema.graphql', '-o',
               'docs/graphqlapi'], stdout=PIPE, stderr=PIPE)
    p.communicate()[0]

    if p.returncode != 0:
        print("Failed to generate graphqlapi docs.")
        exit(1)
