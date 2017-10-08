import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import Sprint


class SprintType(SQLAlchemyObjectType):

    class Meta:
        model = Sprint
        interfaces = (relay.Node,)
        name = model.__name__


class SprintQuery(BaseQuery):
    sprints = graphene.List(SprintType)

    def resolve_sprints(self, args, context, info):
        query = SprintType.get_query(context)
        return query.all()
