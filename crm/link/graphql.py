import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import Link


class LinkType(SQLAlchemyObjectType):

    class Meta:
        model = Link


class LinkQuery(BaseQuery):
    links = graphene.List(LinkType)

    def resolve_links(self, args, context, info):
        query = LinkType.get_query(context)
        return query.all()
