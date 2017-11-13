import graphene
from graphene.types.inputobjecttype import InputObjectType


class OrganizationArguments(InputObjectType):
    uid = graphene.String()
    name = graphene.String()
    description = graphene.String()
    emails = graphene.String()
    telephones = graphene.String()
    tasks = graphene.List('crm.apps.task.graphql.arguments.TaskArguments')
    comments = graphene.List('crm.apps.comment.graphql.arguments.CommentArguments')
    messages = graphene.List('crm.apps.message.graphql.arguments.MessageArguments')
    users = graphene.List('crm.apps.user.graphql.arguments.UserArguments')
    links = graphene.List('crm.apps.link.graphql.arguments.LinkArguments')
    owner_id = graphene.String()
    parent_id = graphene.String()


class CreateOrganizationArguments(OrganizationArguments):
    name = graphene.String(required=True)


class UpdateOrganizationArguments(OrganizationArguments):
    uid = graphene.String(required=True)
