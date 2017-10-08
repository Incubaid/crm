import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import Company


class CompanyType(SQLAlchemyObjectType):

    class Meta:
        model = Company
        interfaces = (relay.Node,)
        name = model.__name__


class CompanyQuery(BaseQuery):
    companies = graphene.List(CompanyType)

    def resolve_comments(self, args, context, info):
        query = CompanyType.get_query(context)
        return query.all()
