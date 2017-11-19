import os

DEBUG = True
Testing = True

DB_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'dev.db'
    )
)

SQLALCHEMY_DATABASE_URI = os.getenv(
    'SQLALCHEMY_DATABASE_URI',
    'sqlite:///%s' % DB_PATH
)

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_RECORD_QUERIES = True

CACHE_BACKEND_URI = 'memory://'

DATA_DIR = 'data'

SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', None)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", None)
