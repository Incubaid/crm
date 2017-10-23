import graphene
from graphene.types.inputobjecttype import InputObjectType


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


class AddressArguments(InputObjectType):
    street_number = graphene.String()
    street_name = graphene.String()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    zip_code = graphene.String()
