import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import Project


class ProjectType(SQLAlchemyObjectType):

    class Meta:
        model = Project
        interfaces = (relay.Node,)
        name = model.__name__


class ProjectQuery(BaseQuery):
    projects = graphene.List(ProjectType)

    def resolve_projects(self, args, context, info):
        query = ProjectType.get_query(context)
        return query.all()
