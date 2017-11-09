import graphene
from graphene.types.inputobjecttype import InputObjectType


class SprintArguments(InputObjectType):
    uid = graphene.String()
    name = graphene.String()
    description = graphene.String()
    start_date = graphene.String()
    deadline = graphene.String()
    contacts = graphene.List('crm.apps.contact.graphql.arguments.ContactArguments')
    tasks = graphene.List('crm.apps.task.graphql.arguments.TaskArguments')
    comments = graphene.List('crm.apps.comment.graphql.arguments.CommentArguments')
    messages = graphene.List('crm.apps.message.graphql.arguments.MessageArguments')
    links = graphene.List('crm.apps.link.graphql.arguments.LinkArguments')
    owner_id = graphene.String()
    project_id = graphene.String()


class CreateSprintArguments(SprintArguments):
    name = graphene.String(required=True)


class UpdateSprintArguments(SprintArguments):
    uid = graphene.String(required=True)
