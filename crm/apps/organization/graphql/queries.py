import graphene

from .types import OrganizationType
from crm.graphql import BaseQuery


class OrganizationQuery(BaseQuery):
    organizations = graphene.List(OrganizationType)

    def resolve_organizations(self, args, context, info):
        query = OrganizationType.get_query(context)
        return query.all()
