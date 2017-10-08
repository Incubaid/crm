import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Contact


class ContactType(SQLAlchemyObjectType):

    class Meta:
        model = Contact


class ContactQuery(graphene.AbstractType):
    contacts = graphene.List(ContactType)

    def resolve_contacts(self, args, context, info):
        query = ContactType.get_query(context)
        return query.all()
