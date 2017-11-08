import graphene

from .types import PassportType
from crm.graphql import BaseQuery


class PassportQuery(BaseQuery):
    passports = graphene.List(PassportType)

    def resolve_passports(self, args, context, info):
        query = PassportType.get_query(context)
        return query.all()
