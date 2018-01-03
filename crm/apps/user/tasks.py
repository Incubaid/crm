# RQ tasks


def update_last_login_time(user_id, time):
    """
    Update last login time.
    Used in iyo middleware
    :param user_id: user ID
    :param time: last login time
    """
    from crm.db import db
    from .models import User

    u = User.query.filter_by(id=user_id).first()
    u.last_login = time
    db.session.add(u)
    db.session.commit()

