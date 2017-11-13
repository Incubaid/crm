from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.project.models import Project


class ProjectType(SQLAlchemyObjectType):

    class Meta:
        model = Project
        interfaces = (relay.Node,)
        name = model.__name__
