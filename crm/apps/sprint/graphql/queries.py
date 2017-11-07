import graphene

from .types import SprintType

from crm.graphql import BaseQuery


class SprintQuery(BaseQuery):
    sprints = graphene.List(SprintType)

    def resolve_sprints(self, args, context, info):
        query = SprintType.get_query(context)
        return query.all()
