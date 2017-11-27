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
STATIC_DIR = os.path.abspath(
    os.path.join(
        dirname(dirname(__file__)),
        'static'
    )
)

STATIC_URL_PATH = "/" + os.path.relpath(STATIC_DIR)

IMAGES_DIR = os.path.join(STATIC_DIR, "uploads", "images")

ATTACHMENTS_DIR = os.path.join(STATIC_DIR, "uploads", "attachments")

DATA_DIR = os.getenv('DATA_DIR')

CACHE_BACKEND_URI = os.getenv('CACHE_BACKEND_URI', "http://127.0.0.1:6379")

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL')

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

######################
# Leave as the last line
########################

# Load env settings into globals
settings_module = 'crm.settings_%s' % os.getenv("ENV", 'dev')
env_settings = import_module(settings_module).__dict__
globals().update(env_settings)
