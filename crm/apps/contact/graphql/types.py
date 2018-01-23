from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.contact.models import Contact
from crm.graphql import CrmType


class ContactType(CrmType, SQLAlchemyObjectType):

    class Meta:
        model = Contact
        interfaces = (relay.Node,)
        name = model.__name__

        # CrmType adds author_original, author_last objects rather than ids
        exclude_fields = (
            'author_original_id',
            'author_last_id'
        )
