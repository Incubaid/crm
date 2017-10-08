import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Task


class TaskType(SQLAlchemyObjectType):

    class Meta:
        model = Task


class TaskQuery(graphene.AbstractType):
    tasks = graphene.List(TaskType)

    def resolve_tasks(self, args, context, info):
        query = TaskType.get_query(context)
        return query.all()
