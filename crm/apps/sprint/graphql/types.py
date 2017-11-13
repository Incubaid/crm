import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.sprint.models import Sprint


class SprintType(SQLAlchemyObjectType):

    class Meta:
        model = Sprint
        interfaces = (relay.Node,)
        name = model.__name__

