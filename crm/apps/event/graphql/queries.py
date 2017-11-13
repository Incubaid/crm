import graphene

from .types import EventType
from crm.graphql import BaseQuery


class EventQuery(BaseQuery):
    events = graphene.List(EventType)

    def resolve_images(self, args, context, info):
        query = EventType.get_query(context)
        return query.all()
