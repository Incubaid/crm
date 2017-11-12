import os

DEBUG = False


SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

SQLALCHEMY_TRACK_MODIFICATIONS = False

DATA_DIR = os.getenv('DATA_DIR', '/opt/code/github/incubaid/data_crm')

CACHE_BACKEND_URI = os.getenv('CACHE_BACKEND_URI')


SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SUPPORT_EMAIL = 'thabeta@greenitglobe.com'
