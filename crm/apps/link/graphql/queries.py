import graphene

from .types import LinkType
from crm.graphql import BaseQuery


class LinkQuery(BaseQuery):
    links = graphene.List(LinkType)

    def resolve_links(self, args, context, info):
        query = LinkType.get_query(context)
        return query.all()
