import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Sprint


class SprintType(SQLAlchemyObjectType):

    class Meta:
        model = Sprint


class SprintQuery(graphene.AbstractType):
    sprints = graphene.List(SprintType)

    def resolve_sprints(self, args, context, info):
        query = SprintType.get_query(context)
        return query.all()
