import graphene
from sqlalchemy.inspection import inspect


class BaseMutation(graphene.ObjectType):
    """
    Base class for all Mutations
    """
    pass


class BaseQuery(graphene.ObjectType):
    """
    Base class for all Queries
    """
    pass

