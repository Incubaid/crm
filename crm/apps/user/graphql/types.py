from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.user.models import User
from crm.graphql import CrmType


class UserType(CrmType, SQLAlchemyObjectType):

    class Meta:
        model = User
        interfaces = (relay.Node,)
        name = model.__name__
        exclude_fields = (
            'author_original_id',
            'author_last_id'
        )
