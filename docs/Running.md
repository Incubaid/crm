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

**Disable IYO integration**

If you're just testing stuff locally, then you may need to run the CRM behind
caddy server otherwise you may need to disable IYO authentication in order for the app
to work locally.
You can do so, by commenting these 2 middlewares in ```middlewares.py``` module
- before_first_request
- authenticate


**Run in Dev Mode**
```
export ENV=dev
python app.py # (if you want DEBUG mode activated)
## OR##
flask run
```
If you want to load fixture data
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
```
flask dumpdata
```

**Load data from json**
```
flask loaddata
```



