# incubaidCRM

## Installation
- clone `https://github.com/Incubaid/crm`
- `pip install -r requirements.txt`

## Start Application
`python3 app.py`
go to localhost:5000/admin

## Development
- Models are defined as SQLAlchemy models in`models.py` file, and the specs are here https://github.com/Incubaid/crm/blob/master/model.md

- Fixtures to be included in fixtures directory
- To register a model in `Flask-Admin`: add it to `dbmodels` list and it'll be autoregisted in the admin

- Tests in tests directory

