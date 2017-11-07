import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.address.graphql.arguments import AddressArguments


class CreateDealArguments(InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    amount = graphene.Float()
    currency = graphene.String(required=True)
    deal_type = graphene.String(required=True)
    closed_at = graphene.String()
    company_id = graphene.String()
    contact_id = graphene.String()
    referral_code = graphene.String()
    shipping_addresses = graphene.List(AddressArguments)


class UpdateDealArguments(CreateDealArguments):
    uid = graphene.String(required=True)
    name = graphene.String()
    currency = graphene.String()
    deal_type = graphene.String()
    deal_state = graphene.String()
    is_paid = graphene.Boolean()