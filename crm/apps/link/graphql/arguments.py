import graphene
from graphene.types.inputobjecttype import InputObjectType


class LinkArguments(InputObjectType):
    uid = graphene.String()
    url = graphene.String()
    labels = graphene.String()
    contact_id = graphene.String()
    user_id = graphene.String()
    deal_id = graphene.String()
    task_id = graphene.String()
    organization_id = graphene.String()
    project_id = graphene.String()
    sprint_id = graphene.String()
    event_id = graphene.String()
    comments = graphene.List('crm.apps.comment.graphql.arguments.CommentArguments')


class CreateLinkArguments(LinkArguments):
    url = graphene.String(required=True)


class UpdateLinkArguments(LinkArguments):
    uid = graphene.String(requied=True)