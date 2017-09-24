import os
import ujson as json
from datetime import datetime

from crm.db import BaseModel, db
from crm import app, migrate

from fixtures import generate_fixtures


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
    """Load tables with data from filesystem."""
    # ensure database directory
    from crm import app
    data_dir = app.config["DATA_DIR"]
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    # Delete all data
    for model in BaseModel.__subclasses__():
        model.query.delete()

    for model in BaseModel.__subclasses__():

        model_dir = os.path.abspath(os.path.join(data_dir, model.__name__))
        for root, dirs, files in os.walk(model_dir):
            for file in files:
                file_path = os.path.abspath(os.path.join(root, file))
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    excluded = []

                    if 'datetime_fields' in data:
                        for field in data['datetime_fields']:
                            data[field] = datetime.strptime(data[field], "%Y-%m-%d %H:%M:%S")
                    for field, value in data.items():
                        if isinstance(value, dict):
                            if 'id' in value:
                                excluded.append(field)
                            else: # enum
                                data[field] = value['name']
                        if isinstance(value, list):
                            excluded.append(field)
                    for field in excluded:
                        data.pop(field)
                    db.session.add(model(**data))
            db.session.commit()
