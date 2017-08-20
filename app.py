from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import os

from models import db
from models import Telephone, Contact, Organization, Company, Deal, Project, Sprint, Task, Comment, Message

dbmodels = [Telephone, Contact, Organization , Company, Deal, Project, Sprint, Task, Comment, Message]
DBPATH = os.path.join(os.getcwd(), "db", "development.db") 
DBPATHPROD = os.path.join(os.getcwd(), "db", "production.db") 

config = {
    "SQLALCHEMY_DATABASE_URI":"sqlite:///{}".format(DBPATH),
    "SQLALCHEMY_ECHO": True,
    "SQLALCHEMY_RECORD_QUERIES": True,
}
app = Flask(__name__)
app.config = {**app.config, **config}
db.init_app(app)


try:
    db.create_all(app=app)
    # db.session.commit()
except Exception as e: # db already exists
    raise

@app.route("/")
def hello():
    return "hello world"


if __name__ == "__main__":
    admin = Admin(app, name="CRM")
    for m in dbmodels:
        admin.add_view(ModelView(m, db.session))
    app.run()