import enum
import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.country.countries import countries
from crm.graphql import BaseArgument

countries = enum.Enum('CountriesEnum', {v.replace(' ', '').replace('-', '').replace(',', '').replace("'", '').replace('.', '').replace('(', '').replace(')',''):k for k,v in countries.items()})


class CountryArguments(InputObjectType, BaseArgument):
    """
    Country Arguments
    """
    name = graphene.Enum.from_enum(countries)()

# ****************************************************
# NO NEED FOR CREATE/UPDATE COUNTRY                   *
# *****************************************************
