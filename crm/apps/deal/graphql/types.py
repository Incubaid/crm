import graphene
from graphene import relay, ObjectType
from graphene_sqlalchemy.types import SQLAlchemyObjectType

from crm.apps.deal.models import Deal


class DealType(SQLAlchemyObjectType):
    # object.id in graphene contains internal
    # representation of id.
    # we add another uid field that we fill
    # with original object.id
    uid = graphene.String()

    class Meta:
        model = Deal
        interfaces = (relay.Node,)
        name = model.__name__


class DealStatsType(ObjectType):
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

    class Meta:
        interfaces = (relay.Node,)
        name = 'dealStats'
