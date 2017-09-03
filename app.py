
import sys
import os
from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_graphql import GraphQLView
from models import db
from schema import schema
from models import Telephone, Email, Contact, Company, Organization, Deal, Link, Project, Sprint, Task, Comment, Message
from views import *
from fixtures import do_fixtures

dbmodels = [Company, Contact, Organization, Deal, Project, Sprint, Task, ]
extramodels = [Telephone, Email,
               Link, Comment, Message]
DBDIR = os.path.join(os.getcwd(), "db")


if not os.path.exists(DBDIR):
    os.mkdir(DBDIR)

development = True

DBPATHDEV = os.path.join(os.getcwd(), "db", "development.db")
DBPATHPROD = os.path.join(os.getcwd(), "db", "production.db")
FIXTURES = os.getenv("BOOTSTRAPWITHFIXTURES", False)
DBPATH = DBPATHDEV

if development is False:
    DBPATH = DBPATHPROD


config = {
    "SQLALCHEMY_DATABASE_URI": "sqlite:///{}".format(DBPATH),
    "SQLALCHEMY_ECHO": True,
    "SQLALCHEMY_RECORD_QUERIES": True,
}

app = Flask(__name__)
app.jinja_env.globals.update(getattr=getattr, hasattr=hasattr, type=type)
app.secret_key = "dmdmkey"
app.config = {**app.config, **config}
db.app = app
db.init_app(app)
migrate = Migrate(app, db)


if __name__ == "__main__":
    if FIXTURES:
        try:
            os.remove(DBPATH)
        except:
            pass

        try:
            db.create_all(app=app)
            db.session.commit()
        except Exception as e:  # db already exists
            raise
        try:
            do_fixtures()
        except Exception as e:
            raise
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
    app.run(debug=True)
