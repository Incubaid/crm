import os
import ujson as json

from sqlalchemy_utils import create_database, database_exists

from crm.db import BaseModel, db, RootModel
from crm import app

from fixtures import generate_fixtures


@app.cli.command()
def createdb():
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all(app=app)
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
        # Root models are 'Company', 'Contact', 'Deal', 'Sprint', 'Project', 'Organization','User'
        if not model in RootModel.__subclasses__():
            continue

        model_dir = os.path.abspath(os.path.join(data_dir, model.__name__))
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)

        for obj in model.query.all():
            obj_as_str = str(obj).replace('/', '_')
            if len(obj_as_str) > 100:
                obj_as_str = obj_as_str[:100]

            record_path = os.path.abspath(os.path.join(model_dir, '%s_%s.json' % (obj.id, obj_as_str)))
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

    # example: {model_name1: model_obj1,model_name12 model_obj2}
    models = {}

    # Initialize our dicts
    for model in BaseModel.__subclasses__():
        models[model.__name__] = model
        added_object_ids[model.__name__] = []

    # Delete all data in db
    for model in models.values():
        model.query.delete()

    # START loading
    for model in models.values():
        # Root models are 'Company', 'Contact', 'Deal', 'Sprint', 'Project', 'Organization','User'
        if not model in RootModel.__subclasses__():
            continue

        model_dir = os.path.abspath(os.path.join(data_dir, model.__name__))

        for root, dirs, files in os.walk(model_dir):
            for file in files:
                file_path = os.path.abspath(os.path.join(root, file))
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    objects = model.from_dict(data)
                    for obj in objects:
                        if obj.id in added_object_ids[obj.__class__.__name__]:
                            continue
                        added_object_ids[obj.__class__.__name__].append(obj.id)
                        db.session.add(obj)
            db.session.commit()
