import os

DEBUG = True

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dev.db'))

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % DB_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_RECORD_QUERIES = True
