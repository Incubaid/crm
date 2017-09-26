import os
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


DATA_DIR = 'data'

# ../crm.
STATIC_DIR = os.path.abspath(os.path.join(
    dirname(dirname(__file__)), 'static'))
STATIC_URL_PATH = "/" + os.path.relpath(STATIC_DIR)
IMAGES_DIR = os.path.join(STATIC_DIR, "uploads", "images")

######################
# Leave as the last line
########################

exec("from crm.settings_%s import *" % os.getenv("ENV", 'dev'))

if not globals()['SQLALCHEMY_DATABASE_URI']:
    print('Missing SQLALCHEMY_DATABASE_URI')
    exit(1)
