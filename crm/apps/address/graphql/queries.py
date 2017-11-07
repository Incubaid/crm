import graphene

from crm.apps.address.graphql.types import AddressType
from crm.graphql import BaseQuery


class AddressQuery(BaseQuery):
    addresses = graphene.List(AddressType)

    def resolve_links(self, args, context, info):
        query = AddressType.get_query(context)
        return query.all()
