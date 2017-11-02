# Update Production procedures

- Deploy from ```production``` branch
- After any change to our [graphql](graphql.org/learn/) api, regenerate [graphql](graphql.org/learn/) api usig ```generate_graphql_docs``` then commit new docs


- **Postgres**
    - Backup postgres database or ensure a recent version of postgres backup

- **Caddy**
    - Update ```caddy``` config with the latest config if any
    - stop and start caddy with new config
        ```
        echo **START**;ulimit -n 8192; /opt/bin/caddy -conf=/opt/cfg/caddy.cfg  -agree && echo **OK** || echo **ERROR**
        ```
- **CRM**
    - check where is ```DATA_DIR``` in ```crm.settings_prod.py``` and backup this DIR
        - **`Warning`** ```DATA_DIR``` settings may have been overridden by `export DATA_DIR={custom_path}`

    - make sure you're in production branch and pull new production code
    - stop crm
    - backup data by running ```flask dumpdata``` and take another copy `DATA_DIR`
    - runt script `./prepare.sh --prod` to install all needed requirements or refer to [Installation](Installation.md) page
    - run DB migrations ```flask db upgrade``` to run migrations and update Physical DB
    - make sure you can dumpdata correctly using ```flask dumpdata``` and take a 3rd copy of data for ```crm.settings.DATA_DIR```
    - Run
      ```
      /opt/code/github/incubaid/crm# echo **START**;cd /opt/code/github/incubaid/crm;export SQLALCHEMY_DATABASE_URI=postgresql://user:pass@host:5432/db;export CACHE_BACKEND_URI=redis://{ip}:{port}/{db_number};export ENV=prod;export FLASK_APP=app.py;flask db upgrade; uwsgi --ini uwsgi.ini && echo **OK** || echo **ERROR**

      ```
