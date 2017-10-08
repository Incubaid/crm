import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Link


class LinkType(SQLAlchemyObjectType):

    class Meta:
        model = Link


class LinkQuery(graphene.AbstractType):
    links = graphene.List(LinkType)

    def resolve_links(self, args, context, info):
        query = LinkType.get_query(context)
        return query.all()
