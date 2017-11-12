import graphene

from sqlalchemy import or_


class BaseMutation(graphene.ObjectType):
    """
    Base class for all Mutations
    """
    pass


class BaseQuery(graphene.ObjectType):
    """
    Base class for all Queries
    """



    @staticmethod
    def resolve_query(model, *args, **kwargs):
        """
        firstname: 'or(ali,toto)' 
        firstname: 'contains(ali)'
        firstname: 'like(ali%)'
        firstname: 'sss)'
        firstname: '~sss'
        firstname: 'null' 
        firstname: '~null' 
        firstname: 'in(ali, 'soso')'
        firstname: '~in(ali, 'soso')'
        
        created_at: '>=(1999-02-02)'
        
        
        
        :param model: 
        :param args: 
        :param kwargs: 
        :return: 
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
