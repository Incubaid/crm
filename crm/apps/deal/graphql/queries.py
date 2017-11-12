import graphene
from graphene import relay
from graphene_sqlalchemy.fields import SQLAlchemyConnectionField

from crm.apps.deal.graphql.arguments import DealArguments
from crm.apps.deal.models import Deal
from .types import DealType
from crm.graphql import BaseQuery


class DealQuery(BaseQuery):
    """
    we have 2 queries here Deal and Deals
    """

    # no need for resplve_Deals function here
    deals = SQLAlchemyConnectionField(
        DealType,
        DealArguments.fields()

    )

    # Deal query to return one Deal and takes (uid) argument
    # uid is the original object.id in db
    deal = graphene.Field(DealType, uid=graphene.String())

    def resolve_deal(self, context, uid):
        return DealType.get_query(context).filter_by(id=uid).first()

    def resolve_deals(
        self,
        context,
        *args,
        **kwargs
    ):

        return BaseQuery.resolve_query(Deal, **kwargs)

    class Meta:
        interfaces = (relay.Node,)
