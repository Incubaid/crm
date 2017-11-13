import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.address.graphql.arguments import AddressArguments
from crm.apps.comment.graphql.arguments import CommentArguments
from crm.apps.contact.graphql.arguments import ContactArguments
from crm.apps.deal.graphql.arguments import DealArguments
from crm.apps.link.graphql.arguments import LinkArguments
from crm.apps.message.graphql.arguments import MessageArguments
from crm.apps.tag.graphql.arguments import TagArguments
from crm.apps.task.graphql.arguments import TaskArguments


class CompanyArguments(InputObjectType):
    uid = graphene.String()
    name = graphene.String()
    description = graphene.String()
    vatnumber = graphene.String()
    website = graphene.String()
    emails = graphene.String()
    telephones = graphene.String()
    owner = graphene.Argument('crm.apps.user.graphql.arguments.UserArguments')
    ownerbackup = graphene.Argument('crm.apps.user.graphql.arguments.UserArguments')

    deals = graphene.List(DealArguments)
    comments = graphene.List(CommentArguments)
    tasks = graphene.List(TaskArguments)
    messages = graphene.List(MessageArguments)
    links = graphene.List(LinkArguments)
    contacts = graphene.List(ContactArguments)

    tags = graphene.List(TagArguments)
    addresses = graphene.List(AddressArguments)


class CreateCompanyArguments(CompanyArguments):
    name = graphene.String(required=True)


class UpdateCompanyArguments(CompanyArguments):
    uid = graphene.String(required=True)
