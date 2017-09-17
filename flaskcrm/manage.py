
import sys
import os
import ujson as json
from datetime import datetime
from sqlalchemy_utils import drop_database, create_database, database_exists 
from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_graphql import GraphQLView
from models import db
from schema import schema
from models import *
from views import *
from flask_admin.helpers import get_url
from flask_script import Manager
import settings

dbmodels = [User, Company, Contact, Organization, Deal,Project, Sprint, Task]
extramodels = [Telephone, Email,Link, Comment, Message]


app = Flask(__name__)
manager = Manager(app)
app.config.from_pyfile("settings.py")
if os.getenv("EXTRA_CONFIG", False):
    app.config.from_envvar("EXTRA_CONFIG")
    print(app.config)
app.secret_key = app.config['SECRET_KEY']


app.jinja_env.globals.update(
    getattr=getattr, hasattr=hasattr, type=type, len=len, get_url=get_url)


db.app = app
db.init_app(app)
migrate = Migrate(app, db)


def main(host, port):
    app.add_url_rule(
        '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    admin = Admin(app, name="CRM", template_mode="bootstrap3", url="/")

    for m in dbmodels:
        viewname = m.__name__ + "ModelView"
        viewcls = getattr(sys.modules[__name__], viewname)
        admin.add_view(viewcls(m, db.session))

    for m in extramodels:
        viewname = m.__name__ + "ModelView"
        viewcls = getattr(sys.modules[__name__], viewname)
        admin.add_view(viewcls(m, db.session, category="Extra"))
    debug = not app.config['PRODUCTION']
    app.run(debug=debug, host=host, port=port)


@manager.command
def dropdb():
    """Drop database and tables."""
    if app.config['BACKEND'] == "sqlite3":
        try:
            os.remove(app.config['DBPATH'])
        except:
            raise
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        drop_database(app.config['SQLALCHEMY_DATABASE_URI']) 

    print("Database dropped.")

@manager.command
def createdb():
    """Create database and tables."""
    # ensure database directory
    if app.config['BACKEND'] == 'sqlite3':
        if not os.path.exists(app.config['DBDIR']):
            os.mkdir(app.config['DBDIR'])
    if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
       create_database(app.config['SQLALCHEMY_DATABASE_URI']) 
 
    db.create_all(app=app)
    print("DB created.")


@manager.command
def resetdb():
    """Remove database and create it again."""
    dropdb()
    createdb()
    print("DB Resetted")


@manager.command
def loadfixtures():
    """Load test fixtures into database."""
    from tests.fixtures import generate_fixtures
    generate_fixtures()
    print("Fixtures loaded.")

@manager.option("-h", "--host", help="host", default="0.0.0.0")
@manager.option("-p", "--port", help="port", default=5000)
def startapp(host, port=5000):
    """Starts the Flask-CRM."""
    main(host, int(port))


@manager.command
def dumpdata():
    """Dump data table models into filesystem."""
    # ensure database directory
    data_dir = settings.DATA_DIR
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    for model in dbmodels:
        model_dir = os.path.abspath(os.path.join(data_dir, model.__name__))
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)

        for obj in model.query.all():

            record_path = os.path.abspath(os.path.join(model_dir, '%s_%s.json' % (obj.id, str(obj))))
            data = obj.as_dict()
            with open(record_path, 'w') as f:
                json.dump(data, f, indent=4)

@manager.command
def loaddata():
    """Load tables with data from filesystem."""
    # ensure database directory

    resetdb()
    data_dir = settings.DATA_DIR
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    for model in dbmodels:
        model_dir = os.path.abspath(os.path.join(data_dir, model.__name__))
        for root, dirs, files in os.walk(model_dir):
            for file in files:
                file_path = os.path.abspath(os.path.join(root, file))
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for field in data['datetime_fields']:
                        data[field] = datetime.strptime(data[field], "%Y-%m-%d %H:%M:%S")
                    for field, value in data.items():
                        if isinstance(value, dict):
                            data[field] = value['name']
                    data.pop('datetime_fields')
                    db.session.add(model(**data))
            db.session.commit()



if __name__ == "__main__":
    manager.run()
