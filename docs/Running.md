## Running

**Export Flask APP**

```
export FLASK_APP=app.py
```

**Run these commands First time Only**
- To create migrations folder ```flask db init```
- Create migrations ```flask db migrate```
- Change db ```flask db upgrade```


**Run in Dev Mode**
```
export env=dev
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



