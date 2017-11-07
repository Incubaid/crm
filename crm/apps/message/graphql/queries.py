import graphene

from .types import MessageType

from crm.graphql import BaseQuery


class MessageQuery(BaseQuery):
    messages = graphene.List(MessageType)

    def resolve_messages(self, args, context, info):
        query = MessageType.get_query(context)
        return query.all()
