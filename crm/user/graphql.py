import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import User


class UserType(SQLAlchemyObjectType):

    class Meta:
        model = User


class UserQuery(graphene.AbstractType):
    users = graphene.List(UserType)

    def resolve_users(self, args, context, info):
        query = UserType.get_query(context)
        return query.all()
