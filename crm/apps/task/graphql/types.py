from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.comment.models import Comment


class CommentType(SQLAlchemyObjectType):

    class Meta:
        model = Comment
        interfaces = (relay.Node,)
        name = model.__name__
