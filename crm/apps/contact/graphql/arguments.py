import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.address.graphql.arguments import AddressArguments
from crm.apps.comment.graphql.arguments import CommentArguments
# from crm.apps.deal.graphql.arguments import DealArguments
from crm.apps.link.graphql.arguments import LinkArguments
from crm.apps.message.graphql.arguments import MessageArguments
from crm.apps.task.graphql.arguments import TaskArguments


class ContactSubgroupArguments(InputObjectType):
    groupname = graphene.String()


class ContactArguments(InputObjectType):
    uid = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()
    description = graphene.String()
    bio = graphene.String()
    belief_statement = graphene.String()
    message_channels = graphene.String()
    owner_id = graphene.String()
    ownerbackup_id = graphene.String()
    parent_id = graphene.String()
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


class CreateContactArguments(ContactArguments):
    firstname = graphene.String(required=True)
    lastname = graphene.String(required=True)


class UpdateContactArguments(ContactArguments):
    uid = graphene.String(required=True)

