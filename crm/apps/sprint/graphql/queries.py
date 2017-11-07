import graphene

from .types import TaskType

from crm.graphql import BaseQuery


class TaskQuery(BaseQuery):
    tasks = graphene.List(TaskType)

    def resolve_tasks(self, args, context, info):
        query = TaskType.get_query(context)
        return query.all()
