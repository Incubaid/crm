import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import User


class UserType(SQLAlchemyObjectType):

    class Meta:
        model = User
        interfaces = (relay.Node,)
        name = model.__name__


class UserQuery(BaseQuery):
    users = graphene.List(UserType)

    def resolve_users(self, args, context, info):
        query = UserType.get_query(context)
        return query.all()
