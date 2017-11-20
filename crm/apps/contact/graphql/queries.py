import graphene
from graphene import relay

from crm.apps.contact.graphql.arguments import ContactArguments
from crm.apps.contact.graphql.types import ContactType
from crm.graphql import BaseQuery, CRMConnectionField


class ContactQuery(BaseQuery):
    """
    we have 2 queries here contact and contacts
    """

    # no need for resplve_contacts function here
    contacts = CRMConnectionField(
        ContactType,
        **ContactArguments.fields()

    )
    # contact query to return one contact and takes (uid) argument
    # uid is the original object.id in db
    contact = graphene.Field(ContactType, uid=graphene.String())

    def resolve_contact(self, context, uid):
        return ContactType.get_query(context).filter_by(id=uid).first()


    class Meta:
        interfaces = (relay.Node, )