
import sys
import os
import ujson as json
from datetime import datetime
from sqlalchemy_utils import drop_database, create_database, database_exists 
from flask import Flask, request
from flask_migrate import Migrate
from flask_admin import Admin
from flask_graphql import GraphQLView
from models import db
from schema import schema
from models import *
from views import *
from flask_admin.helpers import get_url
from flask_script import Manager
import requests
import settings

dbmodels = [User, Company, Contact, Organization, Deal,Project, Sprint, Task]
extramodels = [Telephone, Email,Link, Comment, Message]


app = Flask(__name__)
manager = Manager(app)
app.config.from_pyfile("settings.py")

# Extra configurations to override DB connection.
if os.getenv("EXTRA_CONFIG", False):
    app.config.from_envvar("EXTRA_CONFIG")

app.secret_key = app.config['SECRET_KEY']
# Jinja extra globals.
app.jinja_env.globals.update(
    getattr=getattr, hasattr=hasattr, type=type, len=len, get_url=get_url)


db.app = app
db.init_app(app)


@app.before_first_request
def before_first_request():
    # if "graphql" in request.url or "api" in request.url:
    #     return
    caddyoauth = request.cookies.get("caddyoauth")
    if caddyoauth is None: 
        raise RuntimeError("Accessing without oauth info")
    from jose import jwt
    claims = jwt.get_unverified_claims(caddyoauth)
    username = claims['username']
    # print(jwt)
    #{'exp': 1506345564, 'iss': 'itsyouonline', 'username': 'thabet', 'azp': 'simplecrm', 'scope': ['']}
    # print(claims)
    headers = {'Authorization': 'bearer {}'.format(caddyoauth)}
    userinfourl = "https://itsyou.online/api/users/{}/info".format(username)
    response = requests.get(userinfourl, headers=headers)
    response.raise_for_status()
    info = response.json()
    email = info['emailaddresses'][0]['emailaddress']
    emailobjs = Email.query.filter_by(email=email)
    phone = info['phonenumbers'][0]['phonenumber']
    # print(info)
    if emailobjs.count() == 0:
        firstname = info['firstname']
        lastname = info['lastname']
        if not firstname:
            firstname = username
        if not lastname:
            lastname = username
        emailobj = Email(email=email)
        phoneobj = Telephone(number=phone)
        u = User(firstname=firstname, lastname=lastname, emails=[emailobj], telephones=[phoneobj])
        db.session.add(u)
        db.session.commit()
        # print("SIGNED UP USER: ", u)
        # register a new user on the system
# {'validatedemailaddresses': [], 'username': 'thabet', 'validatedphonenumbers': [], 'digitalwallet': [],
#  'phonenumbers': [{'label': 'main', 'phonenumber': '+201143344150'}], 'publicKeys': [], 
# 'emailaddresses': [{'emailaddress': 'thabeta@greenitglobe.com', 'label': 'main'}], 'firstname': '',
#  'addresses': [{'nr': '72', 'label': 'main', 'city': 'Heliopolis / Cairo', 'country': 'Egypt', 'street': 'Nozhastreet', 'other': '', 'postalcode': '11341'}],
#  'lastname': '', 'organizations': None, 'bankaccounts': [], 'ownerof': {'emailaddresses': []}, 'github': {'html_url': '', 'login': '', 'id': 0, 'avatar_url': '', 'name': ''}, 'avatar': [], 'facebook': {'link': '', 'id': '', 'name': '', 'picture': ''}}

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
    if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        drop_database(app.config['SQLALCHEMY_DATABASE_URI']) 

    print("Database dropped.")

@manager.command
def createdb():
    """Create database and tables."""
    # ensure database directory
    if app.config['BACKEND'] == 'sqlite3':
        if not os.path.exists(app.config['DBDIR']):
            os.mkdir(app.config['DBDIR'])
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
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

    for model in dbmodels + extramodels:
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
    data_dir = settings.DATA_DIR
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    for model in dbmodels + extramodels:
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
