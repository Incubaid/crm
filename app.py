import os
from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models import db
from models import Telephone, Contact, Company, Organization, Deal, Link, Project, Sprint, Task, Comment, Message


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

    com1 = Comment(name="acomment", content="Works for me")
    com2 = Comment(name="acomment", content="LGTM")

    u1.comments.append(com1)
    d1.comments.append(com2)

    o1.comments.append(com1)
    db.session.add(com1, com2)
    db.session.commit()


@app.route("/")
def hello():
    return "hello world"


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

    admin = Admin(app, name="CRM")
    for m in dbmodels:
        admin.add_view(ModelView(m, db.session))
    app.run(debug=True)
