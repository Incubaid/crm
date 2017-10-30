import random
import string
import base64

from enum import Enum
from datetime import datetime, date
from collections import OrderedDict

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy import inspect
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql.sqltypes import TIMESTAMP
from crm.admin.mixins import AdminLinksMixin
from sqlalchemy.ext.declarative import declared_attr

db = SQLAlchemy()
db.session.autocommit = True


class RootModel(object):
    pass


class ParentModel(AdminLinksMixin):
    """
    Base Class for all models
    """


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

    @declared_attr
    def author_last_id(cls):
        """
        Last Author is. User id who made the latest modifications
        :return: String Column representing USer ID
        :rtype: db.Column
        """
        return db.Column(
            db.String(5),
            db.ForeignKey('users.id'),
            nullable=True,
        )


    @declared_attr
    def author_original_id(cls):
        """
        Original Author is. User id who made first created record
        :return: String Column representing USer ID
        :rtype: db.Column
        """
        return db.Column(
            db.String(5),
            db.ForeignKey('users.id'),
            nullable=True,
        )

    @property
    def author_last(self):
        from crm.user.models import User
        return User.query.filter_by(id=self.author_last_id).first()

    @property
    def author_original(self):
        from crm.user.models import User
        return User.query.filter_by(id=self.author_original_id).first()

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

    @property
    def datetime_fields(self):
        """
        List ALL datetime fields
        Reason this is important, is that when serializing object into JSON
        we use ujson which serializes dates into epoch
        then when we need to load data from JSON files again, we need to be
        aware of datetime/date fields so that we can deserialize epoch fields

        :return: datetime/date fields
        :rtype: list
        """
        dt_fields = []
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, datetime) or isinstance(value, date):
                dt_fields.append(c.name)
        return dt_fields

    def update_auto_fields(self, update=False):
        """
        Update self.id with self.uid
        Uodate author_original
        Update author_last
        """

        from flask import session
        cur_user = session.get('user') or {} if session else {}

        if not update:
            # Add UID to newly created objects
            self.id = self.uid
            self.author_original_id = cur_user.get('id')
        else:
            self.author_last_id = cur_user.get('id')

    @classmethod
    def encode_graphene_id(cls, id):
        """
        Record ID to Graphene ID
        :param id: Record ID
        :type id: str
        :return: Graphene ID base64 encoded string of ('ModelName:recordID')
        :rtype: str
        """
        return base64.b64encode(
            '{class_name}:{id}'.format(
                class_name=cls.__name__,
                id=id
            )
        )

    @classmethod
    def decode_graphene_id(cls, id):
        """
        Graphene ID to Record ID
        :param id: Graphene ID -> base64 encoded string of ('ModelName:recordID')
        :type id: str
        :return: Record ID
        :rtype: str
        """
        try:
            base64.b64decode(id).split(':')[-1]
        except:
            pass

    def _get_model_from_table_name(self, name):
        """
        model names and classes associations are saved in all db.models 
        using these data, and given a table name, we can return its model class
        :param name: table name
        :type name: str
        :return: model class associated with this table name
        :rtype: db.Model
        """
        for c in self.__class__._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == name:
                return c

    def _get_fk_pk_for(self, model_cls):
        """
        Given model class, return the F.K in that model that is referencing the
        current model object (self) and get the PK being referenced
        :param model_cls: Model class
        :return: F.K in the model_cls, P.K being referenced by F.K in the current object
        :rtype: tuple
        """
        for column_name, sqlalchemy_prop in inspect(model_cls).attrs.items():
            for fk in sqlalchemy_prop.columns[0].foreign_keys:
                table, primary_key = fk.target_fullname.split('.')
                if table == self.__tablename__:
                    return column_name, primary_key

    def as_dict(self, resolve_refs=True):
        """
        If we are serializing object, we serialize all fields then we go into
        F.K fields and Back reference fields and serialize objects there (one level)
        i.e we don't care about their F.Ks nor Back reference fields

        :param resolve_refs: Resolve F.K & Back reference fields into dicts or not
        :type: resolve_refs: bool
        :return: Model object as dict
        :rtype: dict
        """
        data = {}

        m2m = [] # manytomany fields

        for column, sqlalchemy_prop in inspect(self.__class__).attrs.items():
            value = getattr(self, column)
            data[column] = value
            # Foreign key -- resolve it (only 1 level)
            if isinstance(value, db.Model):
                data[column] = value.as_dict(resolve_refs=False)
            # Back references -- resolve them (only 1 level)
            elif isinstance(value, InstrumentedList):
                data[column] = []  # Leave empty if resolve_refs == False
                if resolve_refs:
                    for item in sorted(value, key=lambda obj: str(obj)):
                        data[column].append(item.as_dict(resolve_refs=False))
                    # If The current field actually has a secondary many2many field
                    # append the data to m2m list for further parsing after this loop
                    if hasattr(sqlalchemy_prop, 'secondary') and len(value) > 0:
                        m2m.append({'property': sqlalchemy_prop, 'records': value})

            # Enums are represented as {'name': 'PENDING', 'value': 0}
            # Enum -- We care only about name field.
            elif isinstance(value, Enum):
                data[column] = value.name

        # backrefs that have secondary relationships (manytomany)
        # They pass the previous test  ```elif isinstance(value, InstrumentedList)``` as well
        # but now we are going to get the related data from the manytomany field

        for item in m2m:
            prop = item['property']
            records = item['records']

            table = prop.secondary
            if table is None:
                continue

            model_cls = self._get_model_from_table_name(table.name)
            data[model_cls.__name__] = []
            join_expression = str(prop.secondaryjoin.expression) # i.e 'subgroups.id = contacts_subgroups.subgroup_id'

            # Get field name in the m2m model that refers to data in (records) i.e subgroup_id
            field = join_expression.split('%s.' % model_cls.__table__.name)[-1]
            query_expression1 = getattr(model_cls, field).in_([item.id for item in records])

            # Get F.K in the many2many model that is referencing current object and also the referenced pk
            fk, pk = self._get_fk_pk_for(model_cls)

            # Now getting data from many2any field that belongs to the current object
            result = model_cls.query.filter(and_(query_expression1, getattr(model_cls, fk) == getattr(self, pk))).all()

            for item in result:
                dikt = item.as_dict(resolve_refs=False)
                data[model_cls.__name__].append(dikt)

            # Now append many2many class/table data to the final dictionary
            # when loading data from json/dicts we know that a field belongs to
            # many2many field because this field does not exist in the object being loaded
            # so it's OK
            data[model_cls.__name__].sort(key=lambda d: d['created_at'])

        data['model'] = self.__class__.__name__
        return OrderedDict(sorted(data.items(), key=lambda t: t[0]))

    @staticmethod
    def from_dict(data):
        """
        Passed is a dictionary that represents a model object
        It can contain other dicts (each one is a F.K to another model object)
        It also can contain lists of dicts representing list of another model objects
        that is connected to our model object with back reference relation
        Basically we need to return list of models representing all data in the passed 
        dictionary.

        :param data: Dictionary of model object we want to deserialize into many model objects
        :type data: dict
        :return: list of model objects
        :rtype: list
        """
        all_models = {}

        for model in BaseModel.__subclasses__() + ManyToManyBaseModel.__subclasses__():
            all_models[model.__name__] = model

        def deserialize(data):
            model_name = data.pop('model')
            model = all_models[model_name]()

            not_serialized = []

            for field, value in data.items():
                # ManyToMany fields were added as attributes/keys
                # in the generated json file for certain object
                # yet they don't have same attribute name in the actual model
                # so when we parse and find a field that doesn't exist in a model
                # we assume it's a mnaytomany field and we don't care about the
                # attribute name so we defer its processing by adding it to
                # deserialized list
                if not hasattr(all_models[model_name], field):
                    not_serialized.extend(value)
                    continue
                # Make datetime from epoch -- If field type is TIMESTAMP
                # Remember that when serializing, ujson converts datetime
                # objects to epoch
                prop = getattr(all_models[model_name], field).property
                if hasattr(prop, 'columns') and isinstance(prop.columns[0].type, TIMESTAMP):
                    if value:
                        setattr(model, field, datetime.fromtimestamp(value))
                # defer F.Ks to later
                elif isinstance(value, dict):
                    not_serialized.append(value)
                # defer Back references to later
                elif isinstance(value, list):
                    not_serialized.extend(value)
                else:
                    setattr(model, field, value)
            return model, not_serialized

        serialized = [data]
        deserialized = []

        while serialized:
            data = serialized.pop()
            model, raw = deserialize(data)
            deserialized.append(model)
            serialized.extend(raw)
        return deserialized


class BaseModel(ParentModel):
    """
    Parent class for all models, root models
    ID field is string and it's autogenerated by db hooks when inserting
    new record
    """
    id = db.Column(
        db.String(5),
        primary_key=True
    )


class ManyToManyBaseModel(ParentModel):
    """
    Parent class for many to many fields
    ID field is auto incremented ID
    """

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    IS_MANY_TO_MANY = True
