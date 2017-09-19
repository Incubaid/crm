
import sys
import os
from datetime import datetime
import ujson as json

from sqlalchemy_utils import drop_database, create_database, database_exists
from flask_migrate import Migrate
from flask_script import Manager
from flask_admin import Admin
from flask_graphql import GraphQLView

from fixtures import generate_fixtures
from crm.schema import schema
from crm.views import *
from crm.app import app
from crm.db import db, BaseModel
from sqlalchemy.event import listen


# ##########################################################
# We must import all models to ensure proper creation of DB
############################################################
for root, dir, files in os.walk(os.path.join("crm", "apps")):
    if root.endswith('__') or root == 'crm/apps':
        continue
    exec('from crm.apps.%s.models import *' % root.split('/')[-1])


# ##########################################################
# REgister Before insert hook
############################################################
def generate_id(mapper, connect, target):
    target.id = target.uid

for klass in BaseModel.__subclasses__():
    listen(klass, 'before_insert', generate_id)


db.app = app
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)

@manager.command
def dropdb():
    """
    DROP DATABASE TOTALLY
    """
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if db_uri.startswith('sqlite:///'):
        db_file_path = db_uri.replace('sqlite:///', '')
        if not os.path.isabs(db_file_path):
            db_file_path = os.path.abspath(os.path.join('crm', db_file_path))
        if os.path.exists(db_file_path):
            os.remove(db_file_path)
    else:
        drop_database(db_uri)
    print("Database dropped.")


@manager.command
def createdb():
    """
    CREATE DB TABLES
    """
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if not db_uri.startswith('sqlite:///'):
       create_database(db_uri)
    db.create_all(app=app)
    print("DB created.")


@manager.command
def resetdb():
    """
    DROP DB & CREATE DB
    """
    dropdb()
    createdb()


@manager.command
def loadfixtures():
    """Load test fixtures into database."""
    generate_fixtures()
    print("Fixtures loaded.")


def main(host, port):
    app.add_url_rule(
        '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    admin = Admin(app, name="CRM", template_mode="bootstrap3", url="/")

    for m in BaseModel.__subclasses__():
        if hasattr(m, 'IS_MANY_TO_MANY'):
            continue
        viewname = m.__name__ + "ModelView"
        viewcls = getattr(sys.modules[__name__], viewname)
        if not hasattr(m, 'IS_EXTRA'):
            admin.add_view(viewcls(m, db.session))
        else:
            admin.add_view(viewcls(m, db.session, category="Extra"))
    debug = app.config['DEBUG']
    app.run(debug=debug, host=host, port=port)


@manager.option("-h", "--host", help="host", default="0.0.0.0")
@manager.option("-p", "--port", help="port", default=5000)
def startapp(host, port=5000):
    """Starts the Flask-CRM."""
    main(host, int(port))


@manager.command
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

@manager.command
def loaddata():
    """Load tables with data from filesystem."""
    # ensure database directory

    resetdb()
    data_dir = app.config["DATA_DIR"]
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

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


if __name__ == "__main__":
    manager.run()
