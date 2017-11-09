import graphene
from graphene.types.inputobjecttype import InputObjectType


class CommentArguments(InputObjectType):
    uid = graphene.String()
    content = graphene.String()
    company_id = graphene.String()
    contennt = graphene.String()
    contact_id = graphene.String()
    user_id = graphene.String()
    deal_id = graphene.String()
    task_id = graphene.String()
    organization_id = graphene.String()
    project_id = graphene.String()
    sprint_id = graphene.String()
    link_id = graphene.String()
    event_id = graphene.String()


class CreateCommentArguments(CommentArguments):
    content = graphene.String(required=True)


class UpdateCommentArguments(CommentArguments):
    uid = graphene.String(required=True)
