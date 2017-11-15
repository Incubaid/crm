## Configuration

### Settings files

###### Shared settings between all environments

goes inside `crm.settings.py`

- `STATIC_DIR` static files directory
- `STATIC_URL_PATH` static files URL prefix
- `IMAGES_DIR` where images uploads goes
- `LOGGING_CONF` logging configuration
- `ATTACHMENTS_DIR` Attachments directory for the [Mailin Feature](MailinMailout.md)
###### Development mode settings

goes inside ```crm.settings_dev.py```

- `DEBUG = True` Enable debugging
- `Testing = True` Enable testing mode
- [SQLALCHEMY](https://www.sqlalchemy.org/) debugging options
    - `SQLALCHEMY_TRACK_MODIFICATIONS = True`
    - `SQLALCHEMY_ECHO = True`
    - `SQLALCHEMY_RECORD_QUERIES = True`


###### Production mode settings

goes inside ```crm.settings_prod.py```

- `DEBUG = FALSE` Disable debugging
- [SQLALCHEMY](https://www.sqlalchemy.org/) debugging options
    - `SQLALCHEMY_TRACK_MODIFICATIONS = False`
    - `SQLALCHEMY_ECHO=False` &  `SQLALCHEMY_RECORD_QUERIES=False` no need to add them they're set to `False` by default


###### Environment variables settings
- `export CACHE_BACKEND_URI=redis://{ip}:{port}/{db_number}` to set a [redis](https://redis.io/) cache backend
    > In **production mode**, must be set explicitly to a [redis](https://redis.io/) URL.

    > In **development mode**, Not required to set, but the default Cache will be **memory**

    > In **development mode**  command `flask dumpcache` won't work if Cache backend is **memory**

    > Memory cache in a CRM app process can't be accessed by another process like `flask dumpcache`
    so if you want to use `flask dumpcache` you have to use shared cache like [redis](https://redis.io/)

- `export SQLALCHEMY_DATABASE_URI=postgresql://{user}:{pass}@{ip}:{port}/{db_name}` Use [Postgresql](https://www.postgresql.org/) db
    > In **production mode**, must be set explicitly to an [RDBMS](https://en.wikipedia.org/wiki/Relational_database_management_system) like [Postgres](https://www.postgresql.org/)

    > In **development mode** Not required but default is to use a [Sqlite](https://www.sqlite.org/) db called `db.dev` in root dir

- `export EXCLUDED_MIDDLEWARES=iyo,mw2,mw3` Quickly disable a comma separated list of middlewares

    > In **development mode only** if you want to disable some modules during development like [IYO](https://itsyou.online) authentication middleware
    You just have to provide comma separated list of middleware module names

- `export DATA_DIR={path}` change the path where `flask dumpdata` exports DB data to and `flask loaddata` load data into DB from
    > In **production mode** is set by default to `/opt/code/github/incubaid/data_crm`

    > In **development mode** is set by default to `data` dir under the root directory

- export `SENDGRID_API_KEY` for [Mail In/Out](MailinMailOut.md). 
