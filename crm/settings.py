import os
from importlib import import_module
from os.path import dirname

LOGGING_CONF = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}


# ../crm.
STATIC_DIR = os.path.abspath(os.path.join(
    dirname(dirname(__file__)), 'static'))
STATIC_URL_PATH = "/" + os.path.relpath(STATIC_DIR)
IMAGES_DIR = os.path.join(STATIC_DIR, "uploads", "images")

######################
# Leave as the last line
########################

# Load env settings into globals
settings_module = 'crm.settings_%s' % os.getenv("ENV", 'dev')
env_settings = import_module(settings_module).__dict__
globals().update(env_settings)

if not globals()['SQLALCHEMY_DATABASE_URI']:
    print('Missing SQLALCHEMY_DATABASE_URI')
    exit(1)
