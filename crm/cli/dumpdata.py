import os

import ujson as json

from crm import app
from crm.db import RootModel


@app.cli.command()
def dumpdata():
    """
    Dump data table models into filesystem.
    Only Root models are dumped
    'Company', 'Contact', 'Deal',
    'Sprint', 'Project', 'Organization','User'
    """
    data_dir = app.config["DATA_DIR"]
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for model in RootModel.__subclasses__():
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
                json.dump(data, f, indent=4, sort_keys=True)
