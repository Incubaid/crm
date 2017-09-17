## Installation
```
    virtualenv -p python3 crm_env
    . crm_env/bin/activate

    cd crm/api
    pip3 install -r requirements.pip
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createinitialrevisions # (django-revisions app) creates revisions of each db entry change
    python3 manage.py createsuperuser   #provide username/pass for admin i.e (admin, a12345678)

```

## Where is the DATA (DIR)
- By default Data is serialized into ```JSON``` in ```api/data``` directory
- You can change the location of (DATA) DIR by opening ```crm/settings.py``` and changing ```FIXTURE_DIRS```

## importing All Data in (data) DIR
- RUN command: ```python3 manage.py import_data```

## importing Individual data file
- ```python3 manage.py loaddata {file_path}```
- ```python3 manage.py loaddata data/company/company.json```


## Running

- RUN command : ```python manage.py runserver```
- By default, changes in DB are maintained in memory/cache and not accessible from outside application
- If you want changes to be saved in redis cache, open ```settings.py``` file and add:
    ```python
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": 'redis://172.17.0.2:6379',
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
            },
            "TIMEOUT": None
        }
    }

    ```
- *DON'T FORGET TO CHANGE (LOCAtTION) to refer your redis installation*

## Exporting All Data to (data) DIR
- RUN command : ```python3 manage.py export_data```


## Exporting data (INDIVIDUAL MODELS)

Sometimes you may have changes in Database that you want to export into json
you can export any model using
- ```python manage.py dumpdata {app_name.model_name} --format json --indent 4 > data/{app_name}/{modelname}.json```
- examples:
     - ```python3 manage.py dumpdata contact.contact --format json --indent 4 > data/contact/contact.json```
     - ```python3 manage.py dumpdata contact.ContactEmail --format json --indent 4 > contact/fixtures/contactemail.json```

## Cleaning ALL Django migration files (IF NEEDED)
- RUN command: ``` python manage.py clean_migration_files```
