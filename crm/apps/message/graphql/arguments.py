import graphene
from graphene.types.inputobjecttype import InputObjectType


class MessageArguments(InputObjectType):
    uid = graphene.String()
    title = graphene.String()
    content = graphene.String()
    channel = graphene.String()
    time_tosend = graphene.String()
    time_sent = graphene.String()
    author = graphene.Field('crm.apps.contact.graphql.arguments.ContactArguments')
    contact = graphene.Field('crm.apps.contact.graphql.arguments.ContactArguments')
    user = graphene.Field('crm.apps.user.graphql.arguments.UserArguments')
    deal = graphene.Field('crm.apps.deal.graphql.arguments.DealArguments')
    task = graphene.Field('crm.apps.task.graphql.arguments.TaskArguments')
    organization = graphene.Field('crm.apps.organization.graphql.arguments.OrganizationArguments')
    project = graphene.Field('crm.apps.project.graphql.arguments.ProjectArguments')
    sprint = graphene.Field('crm.apps.sprint.graphql.arguments.SprintArguments')
    event_id = graphene.Field('crm.apps.event.graphql.arguments.EventArguments')
    comments = graphene.List('crm.apps.comment.graphql.arguments.CommentArguments')


class CreateMessageArguments(MessageArguments):
    title = graphene.String(required=True)


class UpdateMessageArguments(MessageArguments):
    uid = graphene.String(requied=True)