import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.company.models import Company
from crm.apps.contact.models import Contact
from crm.apps.deal.models import Deal
from crm.apps.email.models import Email
from crm.apps.link.models import Link
from crm.apps.organization.models import Organization
from crm.apps.project.models import Project
from crm.apps.sprint.models import Sprint
from crm.apps.telephone.models import Telephone
from crm.apps.task.models import Task, TaskTracking
from crm.apps.comment.models import Comment
from crm.apps.message.models import Message
from crm.apps.alert.models import Alert


class TelephoneType(SQLAlchemyObjectType):
    class Meta:
        model = Telephone


class EmailType(SQLAlchemyObjectType):

    class Meta:
        model = Email


class ContactType(SQLAlchemyObjectType):

    class Meta:
        model = Contact


class CompanyType(SQLAlchemyObjectType):

    class Meta:
        model = Company


class OrganizationType(SQLAlchemyObjectType):

    class Meta:
        model = Organization


class DealType(SQLAlchemyObjectType):

    class Meta:
        model = Deal


class TaskType(SQLAlchemyObjectType):

    class Meta:
        model = Task


class TaskTrackingType(SQLAlchemyObjectType):

    class Meta:
        model = TaskTracking


class ProjectType(SQLAlchemyObjectType):

    class Meta:
        model = Project


class SprintType(SQLAlchemyObjectType):

    class Meta:
        model = Sprint


class LinkType(SQLAlchemyObjectType):

    class Meta:
        model = Link


class CommentType(SQLAlchemyObjectType):

    class Meta:
        model = Comment


class MessageType(SQLAlchemyObjectType):

    class Meta:
        model = Message

class AlertType(SQLAlchemyObjectType):

    class Meta:
        model = Alert


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    telephones = graphene.List(TelephoneType)
    emails = graphene.List(EmailType)
    contacts = graphene.List(ContactType)
    companies = graphene.List(CompanyType)
    organizations = graphene.List(OrganizationType)
    deals = graphene.List(DealType)
    links = graphene.List(LinkType)
    projects = graphene.List(ProjectType)
    sprints = graphene.List(SprintType)
    tasks = graphene.List(TaskType)
    comments = graphene.List(CommentType)
    messages = graphene.List(MessageType)
    alerts = graphene.List(AlertType)

    def resolve_telephones(self, args, context, info):
        query = TelephoneType.get_query(context)
        return query.all()

    def resolve_emails(self, args, context, info):
        query = EmailType.get_query(context)
        return query.all()

    def resolve_contacts(self, args, context, info):
        query = ContactType.get_query(context)
        return query.all()

    def resolve_companies(self, args, context, info):
        query = CompanyType.get_query(context)
        return query.all()

    def resolve_organizations(self, args, context, info):
        query = OrganizationType.get_query(context)
        return query.all()

    def resolve_deals(self, args, context, info):
        query = DealType.get_query(context)
        return query.all()

    def resolve_projects(self, args, context, info):
        query = ProjectType.get_query(context)
        return query.all()

    def resolve_sprints(self, args, context, info):
        query = SprintType.get_query(context)
        return query.all()

    def resolve_tasks(self, args, context, info):
        query = TaskType.get_query(context)
        return query.all()

    def resolve_comments(self, args, context, info):
        query = CommentType.get_query(context)
        return query.all()

    def resolve_messages(self, args, context, info):
        query = MessageType.get_query(context)
        return query.all()

    def resolve_links(self, args, context, info):
        query = LinkType.get_query(context)
        return query.all()

    def resolve_alerts(self, args, context, info):
        query = AlertType.get_query(context)
        return query.all()


schema = graphene.Schema(
    query=Query,
    types=[
        TelephoneType,
        EmailType,
        ContactType,
        CompanyType,
        OrganizationType,
        DealType,
        ProjectType,
        TaskType,
        LinkType,
        SprintType,
        CommentType,
        MessageType
    ]
)
