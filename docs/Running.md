## Running

**Export Flask APP**

```
export FLASK_APP=app.py
```

**Run these commands First time Only**
- *ONLY IN CASE OF POSTGRES* : ```flask createdb```
- To create migrations folder ```flask db init```
- Create migrations ```flask db migrate```
- create db tables ```flask db upgrade```


**Run in Dev Mode**

- By default CRM app requires IYO authentication. So a typical setup is to use caddy
in front of CRM app where caddy can do the (IYO) authentication
- If you want to disable (IYO) aut for during development, comment out the ```authenticate()``` method
in ```crm.middlewares```

- To run in development mode
    ```
    export ENV=dev
    python3 app.py # (if you want DEBUG mode activated)
    ## OR##
    flask run
    ```
- If you want to load fixture data
    ```
    flask laodfixtures
    ```

**Run in [Uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/) / production Mode**
```
export POSTGRES_DATABASE_URI='replace-with-postgres-uri'
export ENV=prod
uwsgi --ini uwsgi.ini
```
If you want uwsgi to use virtualenv; edit uwsgi.ini and add ```virtualenv = <path>```

**Dump data into json**
- command : ```flask dumpdata```
- default Directory is set in ```settings.DATA_DIR```


**Load data from json**
- command: ```flask loaddata```




