import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import Comment


class CommentType(SQLAlchemyObjectType):

    class Meta:
        model = Comment
        interfaces = (relay.Node,)
        name = model.__name__


class CommentQuery(BaseQuery):
    comments = graphene.List(CommentType)

    def resolve_comments(self, args, context, info):
        query = CommentType.get_query(context)
        return query.all()
