import os

PRODUCTION = True
DBDIR = os.path.join(os.getcwd(), "db")
DBPATHDEV = os.path.join(os.getcwd(), "db", "development.db")
DBPATHPROD = os.path.join(os.getcwd(), "db", "production.db")
BOOTSTRAPWITHFIXTURES = os.getenv("BOOTSTRAPWITHFIXTURES", False)
RESETDB = os.getenv("RESETDB", False)
DBPATH = DBPATHDEV

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(DBPATH)
SQLALCHEMY_ECHO = True
SQLALCHEMY_RECORD_QUERIES = True

SECRET_KEY = "dmdmkey"

if PRODUCTION is False:
    DBPATH = DBDIR
