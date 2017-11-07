from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.organization.models import Organization


class OrganizationType(SQLAlchemyObjectType):

    class Meta:
        model = Organization
        interfaces = (relay.Node,)
        name = model.__name__
