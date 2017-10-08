import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Project


class ProjectType(SQLAlchemyObjectType):

    class Meta:
        model = Project


class ProjectQuery(graphene.AbstractType):
    projects = graphene.List(ProjectType)

    def resolve_projects(self, args, context, info):
        query = ProjectType.get_query(context)
        return query.all()
