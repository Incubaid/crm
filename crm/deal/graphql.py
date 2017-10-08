import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import Deal


class DealType(SQLAlchemyObjectType):

    class Meta:
        model = Deal
        interfaces = (relay.Node,)
        name = model.__name__


class DealQuery(BaseQuery):
    deals = graphene.List(DealType)

    def resolve_deals(self, args, context, info):
        query = DealType.get_query(context)
        return query.all()
