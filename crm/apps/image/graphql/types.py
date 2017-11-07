from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.image.models import Image


class ImageType(SQLAlchemyObjectType):

    class Meta:
        model = Image
        interfaces = (relay.Node,)
        name = model.__name__
