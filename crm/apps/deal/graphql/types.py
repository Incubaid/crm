import graphene
from graphene.types.datetime import DateTime
from graphene import relay, ObjectType
from graphene_sqlalchemy.types import SQLAlchemyObjectType

from crm.apps.deal.models import Deal
from crm.graphql import CrmType


class DealType(CrmType, SQLAlchemyObjectType):
    class Meta:
        model = Deal
        interfaces = (relay.Node,)
        name = model.__name__

        # CrmType adds author_original, author_last objects rather than ids
        exclude_fields = (
            'author_original_id',
            'author_last_id'
        )


class DealsStatsType(ObjectType):
    start = DateTime()
    end = DateTime()
    total = graphene.Float()
    ambassador = graphene.Float()
    new = graphene.Float()
    interested = graphene.Float()
    confirmed = graphene.Float()
    created = graphene.Float()
    signed = graphene.Float()
    paid = graphene.Float()
    closed = graphene.Float()
    hoster = graphene.Float()
    ito = graphene.Float()
    pto = graphene.Float()
    itft = graphene.Float()
    prepto = graphene.Float()
    lost = graphene.Float()
    target = graphene.Float()

    class Meta:
        interfaces = (relay.Node,)
        name = 'dealsStats'


class OverAllDealStatsType(ObjectType):
    current_round = graphene.Field(DealsStatsType)
    old_rounds = graphene.List(DealsStatsType)

    class Meta:
        interfaces = (relay.Node,)
        name = 'OverAllDealStats'
