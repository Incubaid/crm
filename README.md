# incubaidCRM

## Installation
- clone `https://github.com/Incubaid/crm` 
- checkout to `flaskproject` branch.
- `pip install -r requirements.txt`

## Start Application
- If you want to bootstrap it with some test fixtures 
    `bash runappwithfixtures.sh` which is equivalent to `BOOTSTRAPWITHFIXTURES=TRUE python3 app.py`
- If you have database already just execute `python3 app.py`

## Admin Panel
After starting the application you can access the admin panel from http://localhost:5000/admin

## Development
- Models are defined as SQLAlchemy models in`models.py` file, and the specs are here https://github.com/Incubaid/crm/blob/master/model.md

- Fixtures to be included in fixtures.py
- To register a model in `Flask-Admin`: add it to `dbmodels` list and it'll be autoregisted in the admin



