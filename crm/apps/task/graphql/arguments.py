import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.task.models import TaskType, TaskPriority, TaskState


class TaskArguments(InputObjectType):
    uid = graphene.String()
    title = graphene.String()
    description = graphene.String()
    type = graphene.Enum.from_enum(TaskType)
    priority = graphene.Enum.from_enum(TaskPriority)
    state = graphene.Enum.from_enum(TaskState)

    assignee = graphene.Field('crm.apps.user.graphql.arguments.UserArguments')
    deadline = graphene.String()
    eta = graphene.String()
    time_estimate = graphene.Int()
    time_done = graphene.Int()
    company = graphene.Field('crm.apps.company.graphql.arguments.CompanyArguments')
    contact = graphene.Field('crm.apps.contact.graphql.arguments.ContactArguments')
    user = graphene.Field('crm.apps.user.graphql.arguments.UserArguments')
    deal = graphene.Field('crm.apps.deal.graphql.arguments.DealArguments')
    organization = graphene.Field('crm.apps.organization.graphql.arguments.OrganizationArguments')
    project = graphene.Field('crm.apps.project.graphql.arguments.ProjectArguments')
    sprint = graphene.Field('crm.apps.sprint.graphql.arguments.SprintArguments')
    event = graphene.Field('crm.apps.event.graphql.arguments.EventArguments')
    comments = graphene.List('crm.apps.comment.graphql.arguments.CommentArguments')
    messages = graphene.List('crm.apps.message.graphql.arguments.MessageArguments')
    links = graphene.List('crm.apps.link.graphql.arguments.LinkArguments')


class CreateTaskArguments(TaskArguments):
    title = graphene.String(required=True)


class UpdateTaskArguments(TaskArguments):
    uid = graphene.String(requied=True)