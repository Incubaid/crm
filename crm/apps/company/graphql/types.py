from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.company.models import CompanyTags


class CompanyType(SQLAlchemyObjectType):

    class Meta:
        model = CompanyTags
        interfaces = (relay.Node,)
        name = model.__name__
