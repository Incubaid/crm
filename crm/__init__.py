import os
import warnings
from importlib import import_module

from logging.config import dictConfig

import jinja2
import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from flask import Flask
from flask_admin.helpers import get_url
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin

from crm.graphql import BaseMutation, BaseQuery
from .settings import LOGGING_CONF, STATIC_DIR, IMAGES_DIR, STATIC_URL_PATH
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

        self._app = Flask(
            __name__,
            static_folder=STATIC_DIR,
            static_url_path=STATIC_URL_PATH
        )

        self.ensure_static_dir()
        self.register_template_dirs()
        self.update_jinja_env()
        self.load_settings()
        self.init_db()
        self.inti_admin_app()
        self._graphql_schema = self.init_graphql_schema()

    def ensure_static_dir(self):
        """
        Ensure the existence of static directory (one level above crm dir)
        """
        if not os.path.exists(IMAGES_DIR):
            os.makedirs(IMAGES_DIR)

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
            get_url=get_url,
        )
        self._app.jinja_env.add_extension('jinja2.ext.do')

    def load_settings(self):
        """
        Load project settings
        """
        self._app.config.from_pyfile("./settings.py")
        # New secret key each time app starts, to clear old sessions
        self._app.secret_key = os.urandom(32)


    @staticmethod
    def _load_modules(module_type):
        """
        Walk through the base directory of the application and load the modules based on a specific type

        @param module_type: type of the module, e.g: models, views, graphql...
        """
        base_dir= '{}/'.format(os.path.dirname(os.path.dirname(__file__)))
        for root, _ , files in os.walk(os.path.dirname(__file__)):
            for file_ in files:
                if file_ != '{}.py'.format(module_type):
                    continue
                package = root.replace(base_dir, '').replace('/', '.')
                import_module('{}.{}'.format(package, module_type))


    @staticmethod
    def init_db():
        """
        All models should be imported ahead to ensure the BaseModel.__subclasses__()
        containing all models registered in app.
        and thus we can have a poing where we can get all system models automatically

        Then we can get all models and register before_insert hook
        """
        CRM._load_modules(module_type='models')
        

    def inti_admin_app(self):
        """
        Initialize admin app
        """
        admin_views = __import__(
            'crm.admin.views',
            globals(),
            locals(),
            ['object']
        )

        adminindexview = getattr(
            admin_views,
            'MyAdminIndexView')

        admin = Admin(
            self._app,
            name="CRM",
            index_view=adminindexview(url='/'),
            endpoint='/',
            template_mode="bootstrap3", url="/"
        )

        all_models = {}
        for model in BaseModel.__subclasses__():
            all_models[model.__name__] = model

        with warnings.catch_warnings():
            warnings.filterwarnings(
                'ignore', 'Fields missing from ruleset', UserWarning)
            for main_model in NAV_BAR_ORDER['MAIN']:
                viewname = main_model + "ModelView"
                viewcls = getattr(admin_views, viewname)
                admin.add_view(viewcls(all_models[main_model], db.session))

            for extra_model in NAV_BAR_ORDER['EXTRA']:
                viewname = extra_model + "ModelView"
                viewcls = getattr(admin_views, viewname)
                admin.add_view(
                    viewcls(all_models[extra_model], db.session, category="Extra"))

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
        CRM._load_modules(module_type='views')


    @property
    def graphql_schema(self):
        """
        :return: Graphql Schema 
        :rtype: graphene.Schema
        """
        return self._graphql_schema

    @staticmethod
    def init_graphql_schema():
        """
        Go through all sub apps defined Queries, Types and mutations
        defined in (graphql.py) and register them in one global schema
        """

        # Import all (graphql.py) defined in all sub apps in system
        # After importing we'll have
        # All Queries under ::  BaseQuery.__subclasses__()
        # All Types under :: SQLAlchemyObjectType.__subclasses__()
        # All Mutations under :: BaseMutation.__subclasses__()
        CRM._load_modules(module_type='graphql')

        schema = graphene.Schema(

            # Make dynamic Query class that inherits all defined queries
            query=type(
                'Query',
                tuple(BaseQuery.__subclasses__()),
                {}
            ),

            types=list(SQLAlchemyObjectType.__subclasses__()),

            # Make dynamic Mutations class that inherits all defined mutations
            mutation=type(
                'Mutations',
                tuple(BaseMutation.__subclasses__()),
                {}
            )
        )

        return schema

    @property
    def app(self):
        return self._app


crm = CRM()
app = crm.app

# Initialize app.graphql_schema with apps defined graphql Schema
app.graphql_schema = crm.graphql_schema

db.app = app
db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app)

# python manage.py db init/migrate/upgrade
manager.add_command('db', MigrateCommand)

# Import all sub apps (views.py) to initialize all routes
crm.initialize_all_routes()
