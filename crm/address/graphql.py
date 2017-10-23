import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseQuery
from .models import Address


class AddressType(SQLAlchemyObjectType):

    class Meta:
        model = Address


class AddressQuery(BaseQuery):
    addresses = graphene.List(AddressType)

    def resolve_links(self, args, context, info):
        query = AddressType.get_query(context)
        return query.all()
