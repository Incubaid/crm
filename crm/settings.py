import os

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

######################
# Leave as the last line
########################

exec("from crm.settings_%s import *" % os.getenv("ENV", 'dev'))

if not globals()['SQLALCHEMY_DATABASE_URI']:
    print('Missing SQLALCHEMY_DATABASE_URI')
    exit(1)
