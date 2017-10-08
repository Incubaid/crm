import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Image


class ImageType(SQLAlchemyObjectType):

    class Meta:
        model = Image


class ImageQuery(graphene.AbstractType):
    images = graphene.List(ImageType)

    def resolve_images(self, args, context, info):
        query = ImageType.get_query(context)
        return query.all()
