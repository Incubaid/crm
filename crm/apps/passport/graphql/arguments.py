import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.countries import CountriesEnum


class PassportArguments(InputObjectType):
    passport_fullname = graphene.String()
    passport_number = graphene.String()
    issuance_date = graphene.String()
    expiration_date = graphene.String()
    country = graphene.Enum.from_enum(CountriesEnum)
    contact = graphene.Argument('crm.apps.contact.graphql.arguments.ContactArguments')
    contact_id = graphene.String()


class CreateContactArguments(PassportArguments):
    passport_fullname = graphene.String(required=True)
    passport_number = graphene.String(required=True)
    issuance_date = graphene.String(required=True)
    expiration_date = graphene.String(required=True)


class UpdateContactArguments(PassportArguments):
    uid = graphene.String(required=True)
