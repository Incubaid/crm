import graphene
from graphene import AbstractType
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.fields import SQLAlchemyConnectionField

from sqlalchemy import and_, or_


class BaseMutation(graphene.ObjectType):
    """
    Base class for all Mutations
    """
    pass


class CRMConnectionField(SQLAlchemyConnectionField):
    @classmethod
    def flatten_query(cls, prefix=None, flat_query={}, query={}):
        """
        input like :
        {
            'firstname': 'null',
            'tasks': {'name': 'task'}
        }

        output like:
        {
            'firstname': 'null',
            'tasks.name': 'task'
        }

        :param prefix: when parsing a dict field we pass the parent field name i.e 'tasks'
        :param flat_query: flat dict to be returned at the end after processing
        :param query: original query dict.
        """
        for k, v in query.items():
            if isinstance(v, list):
                flat_query.update(cls.flatten_query(k, flat_query, v[0]))
            elif isinstance(v, dict):
                flat_query.update(cls.flatten_query(k, flat_query, v))
            else:
                field_name = k if not prefix else '%s.%s' % (prefix, k)
                flat_query[field_name] = v
        return flat_query

    @classmethod
    def parse_query(cls, model_cls, field_name, query_str):
        """
        Given a model class field name, and query string like '~sss'
        return SqlAlchemy query for this field

        query_str examples:

        'or(ali,toto)'
        'and(contains(ali), ~alii)'
        'contains(ali)'
        'like(ali%)'
        'sss'
        '~sss'
        'null'
        '~null'
        'in(ali, 'soso')'
        '~in(ali, 'soso')'
        '>=(1999-02-02)'
        ranges
            '[4, 10] => >= 4, & <= 10 inclusive
            ']4, 10[' => >4 & < 10
            '[4, 10[ => >=4 & <10'
            ']4, 10]' => > 4 & < 10


        :param model_cls: Model class
        :param query:
        :type query: str
        :return: SqlAlchemy query
        :rtype: flask_sqlalchemy.BaseQuery
        """

        attr = getattr(model_cls, field_name)
        query_str = query_str.strip(')')

        if query_str == 'null':
            return attr == None
        if query_str == '~null':
            return attr != None
        if query_str.startswith('in('):
            query_str = query_str.replace('in(', '', 1)
            return attr.in_([a.strip() for a in query_str.split(',')])
        if query_str.startswith('~in('):
            query_str = query_str.replace('~in(', '', 1)
            return ~attr.in_([a.strip() for a in query_str.split(',')])
        if query_str.startswith('like('):
            query_str = query_str.replace('like(', '', 1)
            return attr.like(query_str)
        if query_str.startswith('contains('):
            query_str = query_str.replace('contains(', '', 1)
            return attr.contains(query_str)
        if query_str.startswith('~contains('):
            query_str = query_str.replace('~contains(', '', 1)
            return ~attr.contains(query_str)
        if query_str.startswith('[') or query_str.startswith(']'):
            interval = ['[', ']']
            if query_str.startswith(']'):
                interval[0] = ']'
            if query_str.endswith('['):
                interval[1] = '['

            arg1, arg2 = query_str.lstrip(interval[0]).rstrip(interval[1]).strip().split(',')

            q = attr >= arg1

            if interval[0] == ']':
                q = attr > arg1

            if interval[1] == ']':
                q = and_(q, attr <= arg2)
            else:
                q = and_(q, attr < arg2)
            return q
        if query_str.startswith('>='):
            query_str = query_str.replace('>=(', '', 1)
            query_str = query_str.replace('>=', '', 1)
            return attr >= query_str
        if query_str.startswith('<='):
            query_str = query_str.replace('<=(', '', 1)
            query_str = query_str.replace('<=', '', 1)
            return attr >= query_str
        if query_str.startswith('>'):
            query_str = query_str.replace('>(', '', 1)
            query_str = query_str.replace('>', '', 1) # ">0.5" without () is supported too
            return attr >= query_str
        if query_str.startswith('<'):
            query_str = query_str.replace('<(', '', 1)
            query_str = query_str.replace('<', '', 1)
            return attr >= query_str

        if query_str.startswith('and('):
            query_str = query_str.replace('and(', '', 1)
            args = [a.strip() for a in query_str.split(',')]
            args = [cls.parse_query(model_cls, field_name, arg) for arg in args]
            return and_(*[args])

        if query_str.startswith('or('):
            query_str = query_str.replace('or(', '', 1)
            args = [a.strip() for a in query_str.split(',')]
            args = [cls.parse_query(model_cls, field_name, arg) for arg in args]
            return or_(*[args])

        if query_str.startswith('~'):
            return attr != query_str.replace('~', '', 1)

        return attr == query_str

    @classmethod
    def compile_query(cls, model_cls, flat_query, info):
        """
        Given a flat query, return SqlAlchemy query
        :param model_cls: Model class.
        :param flat_query: flat dict to be returned at the end after processing
        :return: SqlAlchemy query
        """
        from graphene_sqlalchemy.utils import get_query
        final_query = get_query(model_cls, info.context)

        for k, v in flat_query.items():

            # If query field is uid or contains uid, replace with (id)
            if 'uid' in k:
                k = k.replace('uid', 'id')

            # these parameters will be already parsed at this point by get_query()
            # they don't exist in models any way
            if k in ['before', 'last', 'after', 'first']:
                continue

            # normal fields, not relation fields
            if '.' not in k:
                filter = cls.parse_query(model_cls, k, v)
            else:
                attrs = k.split('.')
                attr, sub_attr = attrs[0], attrs[1]
                sub_model = model_cls()._get_model_from_table_name(getattr(model_cls, attr).prop.table.name)

                # backeref relation
                if getattr(model_cls, attr).prop.backref:
                    filter = getattr(model_cls, attr).any(cls.parse_query(sub_model, sub_attr, v))
                else:
                    # Foreign keys
                    filter = getattr(model_cls, attr).has(cls.parse_query(sub_model, sub_attr, v))
            if not final_query:
                final_query = model_cls.query.filter(filter)
            else:
                final_query = final_query.filter(filter)
        return final_query

    @classmethod
    def get_query(cls, model, info, **args):
        flat_query = cls.flatten_query(None, {}, args)
        return cls.compile_query(model, flat_query, info,).all()


class BaseQuery(graphene.ObjectType):
    """
    Base class for all Queries
    """
    pass


class BaseArgument(object):
    """
    Base class for all Arguments
    """
    @classmethod
    def fields(cls):
        d = {}

        for attr in dir(cls):
            if attr in ['Argument', 'Field', 'InputField'] or attr.startswith('_'):
                continue
            v = getattr(cls, attr)

            if callable(v) or type(v) == int:
                continue

            d[attr] = v
        return d


class CrmType(object):
    uid = graphene.String()
    author_original = graphene.Field('crm.apps.user.graphql.types.UserType')
    author_last = graphene.Field('crm.apps.user.graphql.types.UserType')
