import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Organization


class OrganizationType(SQLAlchemyObjectType):

    class Meta:
        model = Organization


class OrganizationQuery(graphene.AbstractType):
    organizations = graphene.List(OrganizationType)

    def resolve_organizations(self, args, context, info):
        query = OrganizationType.get_query(context)
        return query.all()
