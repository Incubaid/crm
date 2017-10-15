import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import Message


class MessageType(SQLAlchemyObjectType):

    class Meta:
        model = Message
        interfaces = (relay.Node,)
        name = model.__name__


class MessageQuery(BaseQuery):
    messages = graphene.List(MessageType)

    def resolve_messages(self, args, context, info):
        query = MessageType.get_query(context)
        return query.all()
