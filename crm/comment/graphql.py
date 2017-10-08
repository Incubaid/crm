import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Comment


class CommentType(SQLAlchemyObjectType):

    class Meta:
        model = Comment


class CommentQuery(graphene.AbstractType):
    comments = graphene.List(CommentType)

    def resolve_comments(self, args, context, info):
        query = CommentType.get_query(context)
        return query.all()
