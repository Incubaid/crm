import graphene
from graphene.types.inputobjecttype import InputObjectType


class CommentArguments(InputObjectType):
    uid = graphene.String()
    content = graphene.String()
    company = graphene.Field('crm.apps.company.graphql.arguments.CompanyArguments')
    contact = graphene.Field('crm.apps.contact.graphql.arguments.ContactArguments')
    user = graphene.Field('crm.apps.user.graphql.arguments.UserArguments')
    deal = graphene.Field('crm.apps.deal.graphql.arguments.DealArguments')
    task = graphene.Field('crm.apps.task.graphql.arguments.TaskArguments')
    organization = graphene.Field('crm.apps.organization.graphql.arguments.OrganizationArguments')
    project = graphene.Field('crm.apps.project.graphql.arguments.ProjectArguments')
    sprint = graphene.Field('crm.apps.sprint.graphql.arguments.SprintArguments')
    link = graphene.Field('crm.apps.link.graphql.arguments.LinkArguments')
    event = graphene.Field('crm.apps.event.graphql.arguments.EventArguments')


class CreateCommentArguments(CommentArguments):
    content = graphene.String(required=True)


class UpdateCommentArguments(CommentArguments):
    uid = graphene.String(required=True)
