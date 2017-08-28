
import sys
import os
from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_graphql import GraphQLView
from models import db
from schema import schema
from models import Telephone, Contact, Company, Organization, Deal, Link, Project, Sprint, Task, Comment, Message
from views import *

dbmodels = [Telephone, Contact, Company, Organization,
            Deal, Link, Project, Sprint, Task, Comment, Message]
DBDIR = os.path.join(os.getcwd(), "db")


if not os.path.exists(DBDIR):
    os.mkdir(DBDIR)

development = True

DBPATHDEV = os.path.join(os.getcwd(), "db", "development.db")
DBPATHPROD = os.path.join(os.getcwd(), "db", "production.db")
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
db.session.autocommit = True


def do_fixtures():
    global db
    t1 = Telephone(number="01145533120")
    db.session.add(t1)
    u1 = Contact(firstname="ahmed", lastname="thabet",
                 email="thabeta@dmdm.com")
    u1.telephones = [t1]
    db.session.add(u1)

    t2 = Telephone(number="01145533120")
    db.session.add(t2)
    u2 = Contact(firstname="notahmed", lastname="thabet",
                 email="notthabeta@dmdm.com")
    u2.telephones = [t2]
    db.session.add(u2)

    c1 = Company(name="decompany", description="dmdm inc",
                 email="monster@dmd.inc")
    c1.telephones.append(t1)

    db.session.add(c1)

    o1 = Organization(
        name="dmdmit", description="change the world", email="dmdmit@dmdm.org")
    o1.users.append(u2)

    db.session.add(o1)

    d1 = Deal(name="cairodeal", amount=10000)
    d1.company = c1
    u1.deals.append(d1)

    com1 = Comment(name="a very first comment",
                   content="Works for me prettty long one")
    com2 = Comment(name="second comment", content="LGTM")
    com3 = Comment(name="third comment", content="Can you please update that?")
    com4 = Comment(name="fourth comment", content="Nope won't work.")
    com5 = Comment(name="fifth comment", content="gibberish dmdmdm")
    u1.comments.append(com1)
    d1.comments.append(com2)
    u1.comments.append(com3)
    u2.comments.append(com4)
    u1.comments.append(com5)

    o1.comments.append(com1)
    db.session.add(com1, com2)

    p1 = Project(name="proj1", description="dmdmproj", comments=[com1, com2])
    t1 = Task(title="task1", content="fix dmdm",
              remarks="someremarks")
    t2 = Task(title="task1", content="fix dmdm",
              remarks="someremarks")
    u1.tasks.append(t1)
    u1.tasks.append(t2)

    db.session.add(p1, t1)
    db.session.commit()


if __name__ == "__main__":

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
    admin = Admin(app, name="CRM", template_mode="bootstrap3")

    for m in dbmodels:
        viewname = m.__name__ + "ModelView"
        viewcls = getattr(sys.modules[__name__], viewname)
        admin.add_view(viewcls(m, db.session))
    app.run(debug=True)
