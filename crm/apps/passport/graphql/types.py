from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.passport.models import Passport
from crm.graphql import CrmType


class PassportType(CrmType, SQLAlchemyObjectType):

    class Meta:
        model = Passport
        interfaces = (relay.Node,)
        name = model.__name__

        # CrmType adds author_original, author_last objects rather than ids
        exclude_fields = (
            'author_original_id',
            'author_last_id'
        )

