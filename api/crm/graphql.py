from graphene_django import DjangoObjectType
import graphene
from contact.models import Contact, ContactPhone, ContactEmail
from company.models import CompanyPhone, CompanyEmail, Company
from comment.models import Comment
from contact.graphql import ContactQuery, ContactMutation
from deal.models import Deal

from link.models import Link, LinkLabel

from message.models import MessageContact, Message
from organization.models import Organization
from project.models import Project
from sprint.models import Sprint
from task.models import Task, TaskTracking, TaskAssignment



class CompanyType(DjangoObjectType):
    class Meta:
        model = Company


class CompanyPhoneType(DjangoObjectType):
    class Meta:
        model = ContactPhone


class CompanyEmailType(DjangoObjectType):
    class Meta:
        model = ContactEmail

# Comment
class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

# Deal
class DealsType(DjangoObjectType):
    class Meta:
        model = Deal


class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class LinkLabelType(DjangoObjectType):
    class Meta:
        model = LinkLabel


# Message
class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class MessageContactType(DjangoObjectType):
    class Meta:
        model = MessageContact


# Organization
class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization


# Project
class ProjectType(DjangoObjectType):
    class Meta:
        model = Project

# Sprint
class SprintType(DjangoObjectType):
    class Meta:
        model = Sprint


# Task
class TasksType(DjangoObjectType):
    class Meta:
        model = Task


class TaskTrackingType(DjangoObjectType):
    class Meta:
        model = TaskTracking


class TaskAssignmentType(DjangoObjectType):
    class Meta:
        model = TaskAssignment


class Query(ContactQuery):

    company = graphene.List(CompanyType)
    companyphone = graphene.List(CompanyPhoneType)
    companyemail = graphene.List(CompanyEmailType)
    comment = graphene.List(CommentType)
    deal = graphene.List(DealsType)
    link = graphene.List(LinkType)
    linklabel = graphene.List(LinkLabelType)
    message = graphene.List(MessageType)
    messagecontact = graphene.List(MessageContactType)
    organization = graphene.List(OrganizationType)
    project = graphene.List(ProjectType)
    sprint = graphene.List(SprintType)
    task = graphene.List(TasksType)
    taskassignment = graphene.List(TaskAssignmentType)
    tasktracking = graphene.List(TaskTrackingType)


    @graphene.resolve_only_args
    def resolve_company(self):
        return Company.objects.all()

    @graphene.resolve_only_args
    def resolve_companyemail(self):
        return CompanyEmail.objects.all()

    @graphene.resolve_only_args
    def resolve_companyphone(self):
        return CompanyPhone.objects.all()

    @graphene.resolve_only_args
    def resolve_comment(self):
        return Comment.objects.all()

    @graphene.resolve_only_args
    def resolve_deal(self):
        return Deal.objects.all()

    @graphene.resolve_only_args
    def resolve_link(self):
        return Link.objects.all()

    @graphene.resolve_only_args
    def resolve_linklabel(self):
        return LinkLabel.objects.all()

    @graphene.resolve_only_args
    def resolve_message(self):
        return Message.objects.all()

    @graphene.resolve_only_args
    def resolve_messagecontact(self):
        return MessageContact.objects.all()

    @graphene.resolve_only_args
    def resolve_organization(self):
        return Organization.objects.all()

    @graphene.resolve_only_args
    def resolve_project(self):
        return Project.objects.all()

    @graphene.resolve_only_args
    def resolve_sprint(self):
        return Sprint.objects.all()

    @graphene.resolve_only_args
    def resolve_task(self):
        return Task.objects.all()

    @graphene.resolve_only_args
    def resolve_taskassignment(self):
        return TaskAssignment.objects.all()

    @graphene.resolve_only_args
    def resolve_tasktracking(self):
        return TaskTracking.objects.all()


class Mutations(ContactMutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutations)
