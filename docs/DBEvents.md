## DB Events

- DB Events are functions/callbacks to be executed on responding to some action like Model update/delete/create
- More info on this topic and list of all supported [SQLALCHEMY Events](- List of all [SqlAlchemy events](http://docs.sqlalchemy.org/en/latest/orm/events.html))

**Registering a new hook/event**

- All events are added in package `crm.events`
- Add a new module there with a function call back to be called when some event happen
- Register your function call back by binding it to some event

- Example: `crm.events.catch_db_updates.py`

    ```python
    from sqlalchemy.event import listen

    from crm.db import db


    def catch_db_updates_after_flush(db_session, flush_context):

        db_session.info['changes'] = {
            'updated': db_session.dirty,
            'created': db_session.new,
            'deleted': db_session.deleted
        }

    listen(db.session, 'after_flush', catch_db_updates_after_flush)

    ```

    - **db.session.new** contains all newly created objects but, *No many to many models are included*
    - **db.session.dirty** contains all updated objects
    - **db.session.deleted** contains list of deleted objects


**WARNING**
- DB Events are disabled when you execute command ```flask loaddata``` because usually you don't want
some actions that may manipulate your data to be executed when you try to load a data mirror in physical DB

## Explanation of existing DB events handlers in CRM

**`crm.events.update_auto_fields.py`**

- registers an `after_flush` event callback which gets newly created non many to many models and assign them a unique ID string
and add original author id to model. Also add latest author user id to model

**`crm.events.catch_db_updates.py`**

- registers an `after_flush` event callback which gets values of `db.session.new`, `db.session.dirty` and `db.session.deleted` and cache them
in `db.session.info['changes']` because we need to access these data when the event `after_transaction` is triggered
but during `after_transaction` we have a problem that `db.session.new`, `db.session.dirty` and `db.session.deleted` are all empty, so we cache these data
in temp location where we can access them in the appropriate time


**`crm.events.cache_db_updates.py`**

- registers an `after_transaction` event callback which gets all db updates saved in `db.session.info['changes']`
and adds them to the existing cache backend. so we can keep track of any change to DB in memory and we can dump it into JSON
files in `DATA_DIR` automatically
