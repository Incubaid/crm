import graphene

from .types import ImageType
from crm.graphql import BaseQuery


class ImageQuery(BaseQuery):
    images = graphene.List(ImageType)

    def resolve_images(self, args, context, info):
        query = ImageType.get_query(context)
        return query.all()
