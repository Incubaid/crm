import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.address.graphql.arguments import AddressArguments
from crm.apps.comment.graphql.arguments import CommentArguments
from crm.apps.link.graphql.arguments import LinkArguments
from crm.apps.message.graphql.arguments import MessageArguments
from crm.apps.task.graphql.arguments import TaskArguments


class DealArguments(InputObjectType):
    uid = graphene.String()
    name = graphene.String()
    description = graphene.String()
    value = graphene.Float()
    currency = graphene.String()
    deal_type = graphene.String()
    deal_state = graphene.String()
    closed_at = graphene.String()
    company_id = graphene.String()
    contact_id = graphene.String()
    referrer1 = graphene.Field('crm.apps.contact.graphql.arguments.ContactArguments')
    referrer2 = graphene.Field('crm.apps.contact.graphql.arguments.ContactArguments')

    comments = graphene.List(CommentArguments)
    tasks = graphene.List(TaskArguments)
    messages = graphene.List(MessageArguments)
    links = graphene.List(LinkArguments)


    is_paid = graphene.Boolean()
    referral_code = graphene.String()
    shipping_addresses = graphene.List(AddressArguments)


class CreateDealArguments(DealArguments):
    name = graphene.String(required=True)


class UpdateDealArguments(CreateDealArguments):
    uid = graphene.String(required=False)