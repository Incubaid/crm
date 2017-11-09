import graphene
from graphene.types.inputobjecttype import InputObjectType


class ProjectArguments(InputObjectType):
    uid = graphene.String()
    name = graphene.String()
    description = graphene.String()
    start_date = graphene.String()
    deadline = graphene.String()

    comments = graphene.List('crm.apps.comment.graphql.arguments.CommentArguments')
    messages = graphene.List('crm.apps.message.graphql.arguments.MessageArguments')
    links = graphene.List('crm.apps.link.graphql.arguments.LinkArguments')
    tasks = graphene.List('crm.apps.task.graphql.arguments.TaskArguments')
    sprints = graphene.List('crm.apps.sprint.graphql.arguments.SprintArguments')
    contacts = graphene.List('crm.apps.contact.graphql.arguments.ContactArguments')
    promoter_id = graphene.String()
    guardian_id = graphene.String()


class CreateProjectArguments(ProjectArguments):
    name = graphene.String(required=True)


class UpdateProjectArguments(ProjectArguments):
    uid = graphene.String(requied=True)
