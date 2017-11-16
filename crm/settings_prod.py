import os

DEBUG = False


SQLALCHEMY_TRACK_MODIFICATIONS = False

DATA_DIR = os.getenv('DATA_DIR', '/opt/code/github/incubaid/data_crm')
