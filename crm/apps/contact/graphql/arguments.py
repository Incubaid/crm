import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.address.graphql.arguments import AddressArguments
from crm.apps.comment.graphql.arguments import CommentArguments
from crm.apps.contact.models import Gender
from crm.apps.country.graphql.arguments import CountryArguments
from crm.apps.link.graphql.arguments import LinkArguments
from crm.apps.message.graphql.arguments import MessageArguments
from crm.apps.passport.graphql.arguments import PassportArguments
from crm.apps.task.graphql.arguments import TaskArguments
from crm.graphql import BaseArgument


class ContactSubgroupArguments(InputObjectType):
    groupname = graphene.String()


class ContactArguments(InputObjectType, BaseArgument):
    uid = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()
    gender = graphene.Enum.from_enum(Gender)()
    description = graphene.String()
    bio = graphene.String()
    belief_statement = graphene.String()
    message_channels = graphene.String()
    owner = graphene.Argument('crm.apps.user.graphql.arguments.UserArguments')
    ownerbackup = graphene.Argument('crm.apps.user.graphql.arguments.UserArguments')
    parent = graphene.Argument('crm.apps.contact.graphql.arguments.ContactArguments')
    emails = graphene.String()
    telephones = graphene.String()
    tf_app = graphene.Boolean()
    tf_web = graphene.Boolean()
    referral_code = graphene.String()

    deals = graphene.List('crm.apps.deal.graphql.arguments.DealArguments')
    comments = graphene.List(CommentArguments)
    tasks = graphene.List(TaskArguments)
    messages = graphene.List(MessageArguments)
    links = graphene.List(LinkArguments)

    subgroups = graphene.List(ContactSubgroupArguments)
    addresses = graphene.List(AddressArguments)
    passports = graphene.List(PassportArguments)
    countries = graphene.List(CountryArguments)


class CreateContactArguments(ContactArguments):
    firstname = graphene.String(required=True)
    lastname = graphene.String(required=True)


class UpdateContactArguments(ContactArguments):
    uid = graphene.String(required=True)
