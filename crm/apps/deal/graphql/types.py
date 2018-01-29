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
