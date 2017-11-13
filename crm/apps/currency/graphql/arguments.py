import graphene
from graphene.types.inputobjecttype import InputObjectType


class CurrencyArguments(InputObjectType):
    """
    currency Arguments
    """
    name = graphene.String(required=True)
    value_usd = graphene.Float(required=True)
