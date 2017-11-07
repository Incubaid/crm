import graphene

from .types import CompanyType

from crm.graphql import BaseQuery



class CompanyQuery(BaseQuery):
    companies = graphene.List(CompanyType)

    def resolve_comments(self, args, context, info):
        query = CompanyType.get_query(context)
        return query.all()
