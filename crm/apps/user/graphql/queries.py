import graphene
from .types import UserType

from crm.graphql import BaseQuery


class UserQuery(BaseQuery):
    users = graphene.List(UserType)

    def resolve_users(self, args, context, info):
        query = UserType.get_query(context)
        return query.all()
