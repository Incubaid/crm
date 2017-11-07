from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.link.models import Link


class LinkType(SQLAlchemyObjectType):

    class Meta:
        model = Link

