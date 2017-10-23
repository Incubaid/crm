# Update Production procedures

We do deploy from ```production``` branch
and after any change to our graphql api we regenerate graphql api usig ```generate_graphql_docs```
and we make sure new docs is committed


- **Postgres**
    - Backup postgres database or ensure a recent version of postgres backup

- **Caddy**
    - Update ```caddy``` config with the latest config if any
    - stop and start caddy with new config
        ```
        echo **START**;ulimit -n 8192; /opt/bin/caddy -conf=/opt/cfg/caddy.cfg  -agree && echo **OK** || echo **ERROR**
        ```
- **CRM**
    - check where is ```DATA_DIR``` in ```crm.settings.py``` and backup this DIR
    - make sure you're in production branch and pull new production code
    - stop crm
    - run ```pip install -r requirements.pip``` to update python libs
    - Install any system new dependencies needed
    - backup data by running ```flask dumpdata``` and take another copy of data for ```crm.settings.DATA_DIR```
    - run DB migrations ```flask db upgrade```
    - make sure you can dumpdata correctly using ```flask dumpdata``` and take a 3rd copy of data for ```crm.settings.DATA_DIR```
    - Run
      ```
      /opt/code/github/incubaid/crm# echo **START**;cd /opt/code/github/incubaid/crm;export POSTGRES_DATABASE_URI=postgresql://user:pass@host:5432/db;export ENV=prod;export FLASK_APP=app.py;flask db upgrade; uwsgi --ini uwsgi.ini && echo **OK** || echo **ERROR**

      ```
