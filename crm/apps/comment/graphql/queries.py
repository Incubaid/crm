import graphene

from .types import CommentType
from crm.graphql import BaseQuery


class CommentQuery(BaseQuery):
    comments = graphene.List(CommentType)

    def resolve_comments(self, args, context, info):
        query = CommentType.get_query(context)
        return query.all()
