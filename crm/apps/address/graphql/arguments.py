import graphene
from graphene.types.inputobjecttype import InputObjectType


class AddressArguments(InputObjectType):
    street_number = graphene.String()
    street_name = graphene.String()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    zip_code = graphene.String()
