import graphene
from graphene import relay

from crm.apps.deal.graphql.arguments import DealArguments
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

    def resolve_deal(self, context, uid):
        return DealType.get_query(context).filter_by(id=uid).first()

    class Meta:
        interfaces = (relay.Node,)
