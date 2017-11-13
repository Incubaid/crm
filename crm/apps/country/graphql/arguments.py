import enum
import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.country.countries import countries
from crm.apps.country.countries import CountriesEnum

countries = enum.Enum('CountriesEnum', {k:k for k,v in countries.items()})

class CountryArguments(InputObjectType):
    """
    Country Arguments
    """
    name = graphene.Enum.from_enum(countries)()

# ****************************************************
# NO NEED FOR CREATE/UPDATE COUNTRY                   *
# *****************************************************
