import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Company


class CompanyType(SQLAlchemyObjectType):

    class Meta:
        model = Company


class CompanyQuery(graphene.AbstractType):
    companies = graphene.List(CompanyType)

    def resolve_comments(self, args, context, info):
        query = CompanyType.get_query(context)
        return query.all()
