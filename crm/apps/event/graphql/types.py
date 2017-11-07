from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.event.models import Event


class EventType(SQLAlchemyObjectType):

    class Meta:
        model = Event
        interfaces = (relay.Node,)
        name = model.__name__
