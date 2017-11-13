import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.task.models import Task


class TaskType(SQLAlchemyObjectType):

    uid = graphene.String()

    class Meta:
        model = Task
        interfaces = (relay.Node,)
        name = model.__name__