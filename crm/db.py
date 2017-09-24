import random
import string
from datetime import datetime, date

from flask_sqlalchemy import SQLAlchemy

from crm.admin.mixins import AdminLinksMixin


db = SQLAlchemy()
db.session.autocommit = True


class BaseModel(AdminLinksMixin):
    """
    Base Class for all models
    """

    id = db.Column(
        db.String(5),
        primary_key=True
    )

    created_at = db.Column(
        db.TIMESTAMP,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.TIMESTAMP,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    @property
    def uid(self):
        """
        :return: Unique ID for that record
        :rtype: str
        """
        if self.id:
            return self.id
        while True:
            uid = ''.join(
                random.sample(
                    string.ascii_lowercase + string.digits,
                    5
                )
            )

            if not self.query.filter_by(id=uid).count():
                return uid

    @property
    def short_description(self):
        return "\n".join(
            getattr(self, 'description', '').splitlines()[:3]
        )

    @property
    def short_content(self):
        return "\n".join(
            getattr(self, 'content', '').splitlines()[:3]
        )

    @property
    def created_at_short(self):
        return self.created_at.strftime("%Y-%m-%d")

    @property
    def updated_at_short(self):
        return self.updated_at.strftime("%Y-%m-%d")

    def as_dict(self, resolve_refs=True):
        """
        :param resolve_refs: Resolve F.K fields into dicts or not
        :type: resolve_refs: bool
        :return: Model object as DICT
        :rtype: dict
        """

        d = {
            'datetime_fields': []
        }

        for c in self.__table__.columns:
            k = c.name
            v = getattr(self, c.name)
            d[k] = v

            # ujson only serialize datetimes into epoch
            if isinstance(v, datetime) or isinstance(v, date):
                d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
                d['datetime_fields'].append(k)
            # translate F.Ks to dicts
            elif c.foreign_keys and resolve_refs:
                if getattr(self, k):
                    k = k.replace('_id', '')
                    v = getattr(self, k)
                    if v:
                        d[k] = v.as_dict(resolve_refs=False)
        # list backrefs
        if resolve_refs:
            from sqlalchemy import inspect
            backrefs = set(inspect(self.__class__).attrs.keys()) - set([c.name for c in self.__table__.columns])
            for backref in backrefs:
                d[backref] = d.get(backref, [])
                v = getattr(self, backref)
                try:
                    for item in v:
                        d[backref].append(item.as_dict(resolve_refs=False))
                except TypeError:
                    # not iterable
                    pass
        return d
