# Running

### Development mode

- Default behaviors (can be changed) are:
    - [Sqlite](https://www.sqlite.org/) database is used `dev.db` file is created
    - Memory cache is used

###### Use these commands to quickly run in dev mode
- `export ENV=dev` set development environment *(optional)*
- `export FLASK_DEBUG=1` Set debug mode / *Auto reload when code changes*
- `export FLASK_APP=app.py` Set flask main app module
- Migration commands
    - `flask createdb` Create DB
    - `flask db init` Create migrations dir
    - `flask db migrate` Create migration versions
    - `flask db upgrade` Apply migrations into physical database
- `flask laodfixtures` Load fixtures / *Testing Data* if needed
- run server `flask run`

###### Overriding some defaults in dev mode
- `export CACHE_BACKEND_URI=redis://{ip}:{port}/{db_number}` to set a redis cache backend
- `export SQLALCHEMY_DATABASE_URI=postgresql://{user}:{pass}@{ip}:{port}/{db_name}` Use [Postgresql](https://www.postgresql.org/) db
- `export EXCLUDED_MIDDLEWARES=iyo` Quickly disable [IYO](https://itsyou.online) authentication middleware
- Export & Import
    - `flask dumpdata` dump db into json files
    - `flask loaddata` load json files dump into db
    - by default in development mode, the data directory to export data to or import from is called
    `data` under the root dir of the application, to change this directory use `export DATA_DIR={path}`
##
### Production mode
- `export ENV=prod` set production environment
- `export FLASK_APP=app.py` Set flask main app module
- `export CACHE_BACKEND_URI=redis://172.17.0.3:6379/0` set redis cache backend
- `export SQLALCHEMY_DATABASE_URI=postgresql://postgres:new_password@172.17.0.2:5432/crm` set Database URI
- `uwsgi --ini uwsgi.ini` To run in [Uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/)

**Note**
- In production mode, `DATA_DIR` is set by default to `/opt/code/github/incubaid/data_crm`

##

### Setup Caddy server to allow [IYO](https://itsyou.online) Authentication
We can run our [Flask](https://flask.pocoo.org/) app behind 

The following instructions can be used for production or development modes,
some minor changes will be indicated between 2 environments