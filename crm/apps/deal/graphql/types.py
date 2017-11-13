import graphene
from graphene import relay
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
