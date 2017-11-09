import graphene
from graphene.types.inputobjecttype import InputObjectType


class UserArguments(InputObjectType):
    uid = graphene.String()
    username = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()
    description = graphene.String()
    message_channels = graphene.String()
    emails = graphene.String()
    telephones = graphene.String()
    tasks = graphene.List('crm.apps.task.graphql.arguments.TaskArguments')
    owns_tasks = graphene.List('crm.apps.task.graphql.arguments.TaskArguments')
    comments = graphene.List('crm.apps.comment.graphql.arguments.CommentArguments')
    messages = graphene.List('crm.apps.message.graphql.arguments.MessageArguments')
    links = graphene.List('crm.apps.link.graphql.arguments.LinkArguments')
    owns_contacts = graphene.List('crm.apps.contact.graphql.arguments.ContactArguments')
    owns_backup_contacts = graphene.List('crm.apps.contact.graphql.arguments.ContactArguments')
    owns_companies = graphene.List('crm.apps.company.graphql.arguments.CompanyArguments')
    owns_backup_companies = graphene.List('crm.apps.company.graphql.arguments.CompanyArguments')
    owns_organizations = graphene.List('crm.apps.organization.graphql.arguments.OrganizationArguments')
    owns_sprints = graphene.List('crm.apps.sprint.graphql.arguments.SprintArguments')
    promoter_projects = graphene.List('crm.apps.project.graphql.arguments.ProjectArguments')
    guardian_projects = graphene.List('crm.apps.project.graphql.arguments.ProjectArguments')


class CreateUserArguments(UserArguments):
    username = graphene.String(required=True)


class UpdateUserArguments(UserArguments):
    uid = graphene.String(requied=True)