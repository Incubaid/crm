import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.address.graphql.arguments import AddressArguments


class CreateContactArguments(InputObjectType):
    firstname = graphene.String(required=True)
    lastname = graphene.String()
    description = graphene.String()
    telegram = graphene.String()
    bio = graphene.String()
    emails = graphene.String(required=True)
    telephones = graphene.String(required=True)
    belief_statement = graphene.String()
    owner_id = graphene.String()
    ownerbackup_id = graphene.String()
    parent_id = graphene.String()
    tf_app = graphene.Boolean()
    tf_web = graphene.Boolean()
    country = graphene.String()
    message_channels = graphene.String()
    sub_groups = graphene.List(graphene.String)
    addresses = graphene.List(AddressArguments)


class UpdateContactContactArguments(CreateContactArguments):
    uid = graphene.String(required=True)
    firstname = graphene.String()
    emails = graphene.String()
    telephones = graphene.String()

