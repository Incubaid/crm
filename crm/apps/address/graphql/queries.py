from graphene import relay

from crm.apps.address.graphql.arguments import AddressArguments
from crm.apps.address.graphql.types import AddressType
from crm.graphql import BaseQuery, CRMConnectionField


class AddressQuery(BaseQuery):
    addresses = CRMConnectionField(
        AddressType,
        **AddressArguments.fields()
    )

    class Meta:
        interfaces = (relay.Node,)
