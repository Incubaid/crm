import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import Task


class TaskType(SQLAlchemyObjectType):

    class Meta:
        model = Task
        interfaces = (relay.Node,)
        name = model.__name__


class TaskQuery(BaseQuery):
    tasks = graphene.List(TaskType)

    def resolve_tasks(self, args, context, info):
        query = TaskType.get_query(context)
        return query.all()
