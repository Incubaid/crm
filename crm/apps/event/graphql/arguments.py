import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.comment.graphql.arguments import CommentArguments
from crm.apps.link.graphql.arguments import LinkArguments
from crm.apps.message.graphql.arguments import MessageArguments
from crm.apps.task.graphql.arguments import TaskArguments


class EventArguments(InputObjectType):
    uid = graphene.String()
    title = graphene.String()
    description = graphene.String()
    contact_event_status = graphene.Float()
    event_datetime = graphene.String()

    comments = graphene.List(CommentArguments)
    tasks = graphene.List(TaskArguments)
    messages = graphene.List(MessageArguments)
    links = graphene.List(LinkArguments)
    contacts = graphene.List('crm.apps.contact.graphql.arguments.ContactArguments')


class CreateEventArguments(EventArguments):
    title = graphene.String(required=True)


class UpdateEventArguments(EventArguments):
    uid = graphene.String(required=False)