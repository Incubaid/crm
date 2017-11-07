import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.contact.models import Contact


class ContactType(SQLAlchemyObjectType):
    # object.id in graphene contains internal
    # representation of id.
    # we add another uid field that will return obj.uid property
    # obj.uid returns obj.id if id is set
    uid = graphene.String()

    class Meta:
        model = Contact
        interfaces = (relay.Node,)
        name = model.__name__
