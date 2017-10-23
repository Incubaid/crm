import os

DEBUG = False


SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATA_DIR = '/opt/code/github/incubaid/data_crm'
