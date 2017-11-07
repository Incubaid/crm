from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.address.models import Address


class AddressType(SQLAlchemyObjectType):

    class Meta:
        model = Address


