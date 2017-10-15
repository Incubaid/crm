import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import Image


class ImageType(SQLAlchemyObjectType):

    class Meta:
        model = Image
        interfaces = (relay.Node,)
        name = model.__name__


class ImageQuery(BaseQuery):
    images = graphene.List(ImageType)

    def resolve_images(self, args, context, info):
        query = ImageType.get_query(context)
        return query.all()
