import graphene

from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.address.models import Address
from crm.apps.country.graphql.types import CountryType
from crm.graphql import CrmType


class AddressType(CrmType, SQLAlchemyObjectType):
    country = graphene.Field(CountryType)

    class Meta:
        model = Address
        interfaces = (relay.Node,)
        name = model.__name__

        # CrmType adds author_original, author_last objects rather than ids
        exclude_fields = (
            'author_original_id',
            'author_last_id'
        )