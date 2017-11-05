from crm.db import db

from sqlalchemy.event import listen


def update_auto_fields_before_flush(db_session, flush_context, instances):
    """
    WARNING
    ----------------------------------------------------------
    THIS FUNCTION IS CALLED SEVERAL TIMES.
    WHATEVER IS PUT HERE SHOULD BE IDEMPOTENT OPERATIONS ONLY
    ----------------------------------------------------------

    This is called after u do session.add() before any operation on objects
    It's the right place to manipulate objects we need to alter before trying
    to Hit DB
    
    so we update (id) field and original author here
    we update last author on updated objects
    using model.update_auto_fields() which is idempotent

    :param db_session:  DB session
    :param flush_context:  Internal UOWTransaction object which handles the details of the flush.
    :param instances: affected instances, but usually holds value of None
    """

    # Update ID and original_author
    for created in db_session.new:
        created.update_auto_fields()

    # Update last modifier
    for updated in db_session.dirty:
        if not db_session.is_modified(updated):
            continue
        updated.update_auto_fields(update=True)

listen(db.session, 'before_flush', update_auto_fields_before_flush)
