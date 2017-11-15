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
- `export EXCLUDED_MIDDLEWARES=iyo,mw2,mw3` Quickly disable a comma separated list of middlewares
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
- `export SENDGRID_API_KEY=SENDGRID_KEY_GOES_HERE` for the mailer service. 
- `uwsgi --ini uwsgi.ini` To run in [Uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/)

**Note**
- In production mode, `DATA_DIR` is set by default to `/opt/code/github/incubaid/data_crm`

##

### Setup Caddy server as a reverse proxy to allow [IYO](https://itsyou.online) Authentication

> Ignore this step if you're not familiar with [IYO](https://itsyou.online)
> you can perfectly run CRM behind any reverse proxy of your choice.
> but in this case you'll loose the authentication part of the app
> and you'll need to provide a middleware in the app to do authentication
> See [Writing your own Authentication middleware](AuthenticationMiddleware.md)

We usually run our CRM [Flask](https://flask.pocoo.org/) app behind [Caddy Server](https://caddyserver.com/)
as a reverse proxy since it's powerful and has a list of interesting [Plugins](https://caddyserver.com/download)
one of those is [IYO plugin](https://github.com/itsyouonline/caddy-integration) which can do an out of the box
authentication against [IYO](https://itsyou.online)


- Use [Caddyman](https://github.com/Incubaid/caddyman) to install [Caddy Server](https://caddyserver.com/) with [IYO plugin](https://github.com/itsyouonline/caddy-integration)
- Use the following [Caddy Server](https://caddyserver.com/) configurations assuming you've met these assumptions
    - You already created an [IYO](https://itsyou.online) organization called `crm` with a sub-organization called `crm_users` and you created an app with `client_id` & `client_secret` for this organization
    - [IYO](https://itsyou.online) `client_id` is `crm`
    - [IYO](https://itsyou.online) `client_secret` is `j_V4qVf6dLwWR_jeQJQssss-KymN7D011zFu15H8a4lg9lxde`
    - you want to authenticate only people with membership in `crm.crm_users`
    - you want to skip authentication for some routes like `/api` and `/docs/graphqlapi`
        - in `/api` we handle the authentication through [IYO](https://itsyou.online) manually
        - `/docs/graphqlapi` is public [Graphql](graphql.org/learn/) API docs and we serve it as staticfiles using `browse docs/graphqlapi/index.html`
    - You need to run [Caddy Server](https://caddyserver.com/) on port `10000`
    - You've CRM running on port `5000`
    - ROOT dir for your CRM app is `/opt/code/github/incubaid/crm/`

    ```
    :10000 {
        proxy / localhost:5000 {
            header_upstream Host "localhost:10000"
            except /docs/graphqlapi
        }
        root /opt/code/github/incubaid/crm/
        browse docs/graphqlapi/index.html
        oauth {
            client_id       crm
            client_secret   j_V4qVf6dLwWR_jeQJQssss-KymN7D011zFu15H8a4lg9lxde
            redirect_url    http://localhost:10000/iyo_callback
            authentication_required /             #that means no authentication required
            extra_scopes	user:address,user:email,user:phone,user:memberof:crm.crm_users
            allow_extension api
            allow_extension graphqlapi
            allow_extension html
            allow_extension png

        }
    }
    ```
