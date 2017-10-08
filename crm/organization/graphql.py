import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import Organization


class OrganizationType(SQLAlchemyObjectType):

    class Meta:
        model = Organization
        interfaces = (relay.Node,)
        name = model.__name__


class OrganizationQuery(BaseQuery):
    organizations = graphene.List(OrganizationType)

    def resolve_organizations(self, args, context, info):
        query = OrganizationType.get_query(context)
        return query.all()
