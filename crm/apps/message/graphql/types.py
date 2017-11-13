from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.message.models import Message


class MessageType(SQLAlchemyObjectType):

    class Meta:
        model = Message
        interfaces = (relay.Node,)
        name = model.__name__
