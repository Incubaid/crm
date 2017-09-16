
import sys
import os
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

dbmodels = [User, Company, Contact, Organization, Deal,Project, Sprint, Task]
extramodels = [Telephone, Email,Link, Comment, Message]

app = Flask(__name__)
manager = Manager(app)
app.config.from_pyfile("settings.py")
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
    try:
        os.remove(app.config['DBPATH'])
    except:
        raise


@manager.command
def resetdb():
    """Remove database and create it again."""
    try:
        os.remove(app.config['DBPATH'])
    except:
        raise
    db.create_all(app=app)

    print("DB Resetted")


@manager.command
def createdb():
    """Create database and tables."""
    # ensure database directory
    if not os.path.exists(app.config['DBDIR']):
        os.mkdir(app.config['DBDIR'])

    db.create_all(app=app)
    print("DB created.")


@manager.command
def populate_test_fixtures():
    """Populate database with test fixtures."""
    from tests.fixtures import generate_fixtures
    generate_fixtures()


@manager.option("-h", "--host", help="host", default="0.0.0.0")
@manager.option("-p", "--port", help="port", default=5000)
def startapp(host, port=5000):
    """Starts the Flask-CRM."""
    main(host, int(port))


if __name__ == "__main__":
    manager.run()
