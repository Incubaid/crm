import graphene

from .types import ProjectType

from crm.graphql import BaseQuery


class ProjectQuery(BaseQuery):
    projects = graphene.List(ProjectType)

    def resolve_projects(self, args, context, info):
        query = ProjectType.get_query(context)
        return query.all()
