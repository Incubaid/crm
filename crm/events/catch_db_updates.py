# from sqlalchemy.event import listen
#
# from crm.db import db
#
#
# def catch_db_updates_after_flush(db_session, flush_context):
#     """
#     WARNING
#     ----------------------------------------------------------
#     THIS FUNCTION IS CALLED SEVERAL TIMES.
#     WHATEVER IS PUT HERE SHOULD BE IDEMPOTENT OPERATIONS ONLY
#     ----------------------------------------------------------
#
#
#
#     :param db_session:  DB session
#     :param flush_context:  Internal UOWTransaction object which handles the details of the flush.
#     """
#
#     # db_session.dirty, db_session.created, db_session.new
#     # are vanished during (after_commit) & (after_transaction_end) events
#     # we cache these values in db_session.info['changes'] so we can process them later
#     # after data is written to DB
#
#     # at this point of time we can't call model.as_dict()
#     # and cache this value, because object is not saved in db yet
#     # so we save it in temp location db_session.info['changes']
#     # we catch these cached values on another event (after transaction completes)
#     # we process them there
#
#     db_session.info['changes'] = {
#         'updated': db_session.dirty,
#         'created': db_session.new,
#         'deleted': db_session.deleted
#     }
#
# listen(db.session, 'after_flush', catch_db_updates_after_flush)
