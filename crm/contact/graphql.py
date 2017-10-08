import werkzeug
import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.fields import SQLAlchemyConnectionField
from graphene.relay import Node

from crm.graphql import BaseMutation, BaseQuery
from .models import Contact
from .forms import ContactForm
from crm import db


class ContactType(SQLAlchemyObjectType):
    uid = graphene.String()

    class Meta:
        model = Contact
        interfaces = (relay.Node,)
        name = model.__name__


class ContactQuery(BaseQuery):
    contacts = SQLAlchemyConnectionField(ContactType)
    contact = graphene.Field(ContactType, uid=graphene.String())

    def resolve_contacts(self, context):
        # Manipulate uid field with actual record id in Database
        # Reason is Graphene uses ID field which is base64.b64encode(ModelClass:RecordID)
        res = ContactType.get_query(context).all()
        for e in res:
            e.uuid = e.uid
        return res

    def resolve_contact(self, context, uid):
        return ContactType.get_query(context).filter_by(id=uid).first()

    class Meta:
        interfaces = (Node,)


class CreateContact(graphene.Mutation):
    class Arguments:
        firstname = graphene.String(required=True)
        # lastname = graphene.String(required=True)
        # description = graphene.String()
        # telegram = graphene.String()
        # emails = graphene.String(required=True)
        # phones = graphene.String(required=True)

    contact = graphene.Field(ContactType)
    ok = graphene.Boolean()
    errors = graphene.types.json.JSONString()

    @classmethod
    def mutate(cls, root, context, **kwargs):

        errors = {
            'fields': {},
            'code': 400
        }

        OK = True

        form = ContactForm(werkzeug.MultiDict(kwargs), Contact)
        if not form.validate():
            errors['fields'].update(form.errors)
            return CreateContact(contact=None, ok=False, errors=errors)

        contact = Contact(**form.data)
        db.session.add(contact)
        db.session.commit()

        return CreateContact(contact=contact, ok=True, errors=None)


class ContactMutation(BaseMutation):
    create_contact = CreateContact.Field()
    # update_contact = UpdateContact.Field()
    # delete_contact = DeleteContact.Field()
