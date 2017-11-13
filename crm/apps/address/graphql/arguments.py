import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.country.graphql.arguments import CountryArguments


class AddressArguments(InputObjectType):
    """
    Address Arguments
    """
    street_number = graphene.String()
    street_name = graphene.String()
    city = graphene.String()
    state = graphene.String()
    country = graphene.Argument(CountryArguments)
    zip_code = graphene.String()

# ****************************************************
# NO NEED FOR CREATE/UPDATE ADDRESS                   *
# THIS IS DONE IMPLICITLY THROUGH CONTACT & DEAL APIs *
# *****************************************************
