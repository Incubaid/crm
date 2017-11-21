import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.address.graphql.arguments import AddressArguments
from crm.apps.comment.graphql.arguments import CommentArguments
from crm.apps.currency.graphql.arguments import CurrencyArguments
from crm.apps.deal.models import DealType, DealState
from crm.apps.link.graphql.arguments import LinkArguments
from crm.apps.message.graphql.arguments import MessageArguments
from crm.apps.task.graphql.arguments import TaskArguments
from crm.graphql import BaseArgument

DealType = graphene.Enum.from_enum(DealType)
DealState = graphene.Enum.from_enum(DealState)


class DealArguments(InputObjectType, BaseArgument):
    uid = graphene.String()
    name = graphene.String()
    description = graphene.String()
    value = graphene.String()
    currency = graphene.Argument(CurrencyArguments)
    deal_type = DealType()
    deal_state = DealState()
    closed_at = graphene.String()

    company_id = graphene.String()
    company = graphene.Argument('crm.apps.company.graphql.arguments.CompanyArguments')
    contact_id = graphene.String()
    contact = graphene.Argument('crm.apps.contact.graphql.arguments.ContactArguments')

    referrer1 = graphene.Argument('crm.apps.contact.graphql.arguments.ContactArguments')
    referrer2 = graphene.Argument('crm.apps.contact.graphql.arguments.ContactArguments')
    referrer1_id = graphene.String()
    referrer2_id = graphene.String()

    comments = graphene.List(CommentArguments)
    tasks = graphene.List(TaskArguments)
    messages = graphene.List(MessageArguments)
    links = graphene.List(LinkArguments)

    is_paid = graphene.Boolean()
    referral_code = graphene.String()
    shipping_addresses = graphene.List(AddressArguments)


class CreateDealArguments(DealArguments):
    name = graphene.String(required=True)
    value = graphene.Float(required=True)
    currency = graphene.Argument(CurrencyArguments, required=True)
    deal_type = DealType(required=True)
    deal_state = DealState(required=True)


class UpdateDealArguments(CreateDealArguments):
    uid = graphene.String(required=True)
    value = graphene.Float()