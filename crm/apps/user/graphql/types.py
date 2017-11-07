import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.user.models import User


class UserType(SQLAlchemyObjectType):

    class Meta:
        model = User
        interfaces = (relay.Node,)
        name = model.__name__
