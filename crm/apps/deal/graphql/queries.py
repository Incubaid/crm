import graphene
from graphene import relay
from decimal import Decimal

from crm.apps.deal.graphql.arguments import DealArguments
from crm.apps.deal.graphql.types import DealStatsType
from .types import DealType
from crm.graphql import BaseQuery, CRMConnectionField


class DealQuery(BaseQuery):
    """
    we have 2 queries here Deal and Deals
    """

    # no need for resplve_Deals function here
    deals = CRMConnectionField(
        DealType,
        DealArguments.fields()

    )

    # Deal query to return one Deal and takes (uid) argument
    # uid is the original object.id in db
    deal = graphene.Field(DealType, uid=graphene.String())
    deals_stats = graphene.Field(DealStatsType)

    def resolve_deal(self, context, uid):
        return DealType.get_query(context).filter_by(id=uid).first()

    def resolve_deals_stats(self, context):
        value = Decimal(0.0)
        for deal in DealType.get_query(context).all():
            value += deal.to_usd
        return DealStatsType(total=value)

    class Meta:
        interfaces = (relay.Node,)
