import os

DEBUG = True
Testing = True

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dev.db'))

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///%s' % DB_PATH)

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_RECORD_QUERIES = True

DATA_DIR  = os.getenv('DATA_DIR', 'data')

CACHE_BACKEND_URI = os.getenv('CACHE_BACKEND_URI', 'memory://')