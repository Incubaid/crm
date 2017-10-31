from datetime import datetime

from sqlalchemy.event import listen
from flask import session

from crm import app
from crm.db import BaseModel, RootModel
from .db import db


def before_flush(db_session, flush_context, instances):
    """
    WARNING
    ----------------------------------------------------------
    THIS FUNCTION IS CALLED SEVERAL TIMES.
    WHATEVER IS PUT HERE SHOULD BE IDEMPOTENT OPERATIONS ONLY
    ----------------------------------------------------------
    
    This is called after u do session.add() before any operation on objects
    It's the right place to manipulate objects we need to alter before trying
    to Hit DB
    
    :param db_session:  DB session
    :param flush_context:  Internal UOWTransaction object which handles the details of the flush.
    :param instances: affected instances, but usually holds value of None
    """

    cur_user = session.get('user') or {} if session else {}

    # Update ID and original_author
    for created in db_session.new:
        created.update_auto_fields()

    # Update last modifier
    for updated in db_session.dirty:
        if not db_session.is_modified(updated):
            continue
        updated.update_auto_fields(update=True)


def after_flush(db_session, flush_context):
    """
    WARNING
    ----------------------------------------------------------
    THIS FUNCTION IS CALLED SEVERAL TIMES.
    WHATEVER IS PUT HERE SHOULD BE IDEMPOTENT OPERATIONS ONLY
    ----------------------------------------------------------
    
    
    
    :param db_session:  DB session
    :param flush_context:  Internal UOWTransaction object which handles the details of the flush.
    """

    # db_session.dirty, db_session.created, db_session.new
    # are vanished during (after_commit) & after_transaction_end events
    # we cache these values in db_session.info['changes'] so we can process them later
    # after data is written to DB
    # this because obj.as_dict() may actually do some calls to DB
    # We need to guarantee that obj.as_dict() gets latest data updates to an object
    # at this point, we can't because the data is not written to DB yet, so we cache these values
    # and process them later in an (after_commit or after_transaction_end)event handler

    db_session.info['changes'] = {
        'updated': db_session.dirty,
        'created': db_session.new,
        'deleted': db_session.deleted
    }


def after_transaction(db_session, transaction):
    """
    Intercept transaction after finishes and cache changes
    We need to cache data after being written to DB since some 
    functions called during cache like as_dict() may return invalid data
    if DB is still not up2date
    
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

    for updated in [ e for e in db_session.info['changes']['updated']] + [e for e in db_session.info['changes']['deleted']]:
        # Get all objects referenced by or referencing updated object
        for obj in BaseModel.from_dict(updated.as_dict()):
            if not isinstance(obj, RootModel):
                continue
            obj = obj.__class__.query.filter_by(id=obj.id).first()

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
        obj = obj.__class__.query.filter_by(id=obj.id).first().as_dict()

        if obj in cache['updated']:
            cache['updated'].remove(obj)

        cache['deleted'].append({
            'obj_as_str': str(obj),
            'data': obj
        })

    app.cache.set(now, cache)

    del db_session.info['changes']



listen(db.session, 'before_flush', before_flush)
listen(db.session, 'after_flush', after_flush)
listen(db.session, 'after_transaction_end', after_transaction)
