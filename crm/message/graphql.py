import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Message


class MessageType(SQLAlchemyObjectType):

    class Meta:
        model = Message


class MessageQuery(graphene.AbstractType):
    messages = graphene.List(MessageType)

    def resolve_messages(self, args, context, info):
        query = MessageType.get_query(context)
        return query.all()
