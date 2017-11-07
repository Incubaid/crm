from datetime import datetime

from sqlalchemy.event import listen
from flask import session

from crm import app
from crm.db import BaseModel, RootModel
from crm.db import db


def cache_db_updates_after_transaction(db_session, transaction):
    """
    Intercept transaction after finishes 
    Catch DB changes saved in db_session['info'] by a (before_flush) event
    then process these values and cache actual changes to DB in the current cache backend
    
    We needed to cache data after being written to DB since some 
    functions called during cache like as_dict() may return invalid data
    if DB is still not up2date.
    that's why here is the proper place for such caching after DB is updated

    :param db_session: DB session
    :param transaction: DB transaction
    """
    if not 'changes' in db_session.info:
        return

    cur_user = session.get('user') or {} if session else {}
    username = cur_user.get('username') or 'guest'
    now = str(datetime.now())

    cache = {
        'username': username,
        'created': [],
        'updated': [],
        'deleted': []
    }

    for created in db_session.info['changes']['created']:
        cache['created'].append({
            'obj_as_str': str(created),
            'data': created.as_dict()
        })

    for updated in [e for e in db_session.info['changes']['updated']] + [e for e in
                                                                         db_session.info['changes']['deleted']]:
        # Get all objects referenced by or referencing updated object
        # but all objects are not populated very well
        for obj in BaseModel.from_dict(updated.as_dict()):
            if not isinstance(obj, RootModel):
                continue
            obj = obj.__class__.query.filter_by(id=obj.id).first()

            if obj:
                record = {
                    'obj_as_str': str(obj),
                    'data': obj.as_dict()
                }

                if record not in cache['updated']:
                    cache['updated'].append(record)

    for deleted in db_session.info['changes']['deleted']:
        obj = BaseModel.from_dict(deleted.as_dict())[0]
        if not isinstance(obj, RootModel):
            continue

        cache['deleted'].append({
            'obj_as_str': str(obj),
            'data': obj
        })

    app.cache.set(now, cache)

    del db_session.info['changes']

listen(db.session, 'after_transaction_end', cache_db_updates_after_transaction)
