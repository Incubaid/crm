import os

PRODUCTION = False
DBDIR = os.path.join(os.getcwd(), "db")
DBPATHDEV = os.path.join(os.getcwd(), "db", "development.db")
DBPATHPROD = os.path.join(os.getcwd(), "db", "production.db")
BOOTSTRAPWITHFIXTURES = os.getenv("BOOTSTRAPWITHFIXTURES", False)
RESETDB = os.getenv("RESETDB", False)
DBPATH = DBPATHDEV


if PRODUCTION is True:
    DBPATH = DBPATHPROD

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(DBPATH)
SQLALCHEMY_ECHO = True
SQLALCHEMY_RECORD_QUERIES = True

SECRET_KEY = "dmdmkey"
