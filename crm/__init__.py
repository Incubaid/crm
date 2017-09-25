import os
import warnings

from logging.config import dictConfig

import jinja2

from flask import Flask, request
import requests
from flask_admin.helpers import get_url
from sqlalchemy.event import listen
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin

from .settings import LOGGING_CONF
from .db import BaseModel, db
from crm.admin.config import NAV_BAR_ORDER


class CRM(object):
    """
    A wrapper arounf Flask app that initializes the app in a manner suitable to 
    production.
    """
    def __init__(self):
        from .db import db
        self.initialize_logger()
        self._db = db
        self._app = Flask(__name__)
        self.register_template_dirs()
        self.update_jinja_env()
        self.load_settings()
        self.init_db()
        self.inti_admin_app()

    def register_template_dirs(self):
        """
        Go Through all sub applications under (crm) and if a dir called (templates)
        found, register it as a template directory
        """
        template_dirs = []
        for root, dirs, _ in os.walk('crm'):
            for dir in dirs:
                if not dir == 'templates':
                    continue
                template_dirs.append(os.path.abspath(os.path.join(root, dir)))
        template_loader = jinja2.ChoiceLoader([
            self._app.jinja_loader,
                jinja2.FileSystemLoader(template_dirs),
            ]
        )
        self._app.jinja_loader = template_loader

    def update_jinja_env(self):
        """
        Update JINJA extra globals
        """
        self._app.jinja_env.globals.update(
            getattr=getattr,
            hasattr=hasattr,
            type=type,
            len=len,
            get_url=get_url
        )

    def load_settings(self):
        """
        Load project settings
        """
        self._app.config.from_pyfile("./settings.py")
        self._app.secret_key = self._app.config['SECRET_KEY']

    def init_db(self):
        """
        All models should be imported ahead to ensure the BaseModel.__subclasses__()
        containing all models registered in app.
        and thus we can have a poing where we can get all system models automatically

        Then we can get all models and register before_insert hook
        """
        for root, dir, files in os.walk('crm'):
            for file in files:
                if file != 'models.py':
                    continue
                package = root.replace('/', '.')
                exec('from %s.models import *' % package)

        def generate_id(mapper, connect, target):
            target.id = target.uid

        for klass in BaseModel.__subclasses__():
            listen(klass, 'before_insert', generate_id)

    def inti_admin_app(self):
        """
        Initialize admin app
        """
        admin = Admin(self._app, name="CRM", template_mode="bootstrap3", url="/")

        admin_views = __import__('crm.admin.views', globals(), locals(), ['object'])

        all_models = {}
        for model in BaseModel.__subclasses__():
            all_models[model.__name__] = model

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)
            for main_model in NAV_BAR_ORDER['MAIN']:
                viewname = main_model + "ModelView"
                viewcls = getattr(admin_views, viewname)
                admin.add_view(viewcls(all_models[main_model], db.session))

            for extra_model in NAV_BAR_ORDER['EXTRA']:
                viewname = extra_model + "ModelView"
                viewcls = getattr(admin_views, viewname)
                admin.add_view(viewcls(all_models[extra_model], db.session, category="Extra"))

    @staticmethod
    def initialize_logger():
        """
        Initialize logger with application settings in settings.py
        """
        dictConfig(LOGGING_CONF)

    @staticmethod
    def initialize_all_routes():
        """
        Import all views containing http actions to guarantee all
        routes are initialized
        """
        for root, dirs, files in os.walk('crm'):
            for file in files:
                if file != 'views.py':
                    continue
                package = root.replace('/', '.')
                exec('from %s.views import *' % package)

    @property
    def app(self):
        return self._app


crm = CRM()
app = crm.app

db.app = app
db.init_app(app)



@app.before_first_request
def before_first_request():
    from crm.user.models import User
    # if "graphql" in request.url or "api" in request.url:
    #     return
    caddyoauth = request.cookies.get("caddyoauth")
    if caddyoauth is None: 
        raise RuntimeError("Accessing without oauth info")
    from jose import jwt
    claims = jwt.get_unverified_claims(caddyoauth)
    username = claims['username']

    headers = {'Authorization': 'bearer {}'.format(caddyoauth)}
    userinfourl = "https://itsyou.online/api/users/{}/info".format(username)
    response = requests.get(userinfourl, headers=headers)
    response.raise_for_status()
    info = response.json()
    email = info['emailaddresses'][0]['emailaddress']
    userobjs = User.query.filter(User.emails.contains(email))
    phone = info['phonenumbers'][0]['phonenumber']
    if userobjs.count() == 0:
        firstname = info['firstname']
        lastname = info['lastname']
        if not firstname:
            firstname = username
        if not lastname:
            lastname = username
        u = User(firstname=firstname, lastname=lastname, emails=email, telephones=phone)
        db.session.add(u)
        db.session.commit()

migrate = Migrate(app, db)

manager = Manager(app)

# python manage.py db init/migrate/upgrade
manager.add_command('db', MigrateCommand)

crm.initialize_all_routes()
