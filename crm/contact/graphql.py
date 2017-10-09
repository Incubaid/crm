import werkzeug
import graphene
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.graphql import BaseMutation, BaseQuery, CRMConnectionField, GraphqlError, ErrorType
from .models import Contact
from .forms import ContactForm
from crm import db


class ContactType(SQLAlchemyObjectType):
    # object.id in graphene contains internal
    # representation of id.
    # we add another uid field that we fill
    # with original object.id
    uid = graphene.String()

    class Meta:
        model = Contact
        interfaces = (relay.Node,)
        name = model.__name__


class ContactQuery(BaseQuery):
    """
    we have 2 queries here contact and contacts
    """

    # no need for resplve_contacts function here
    contacts = CRMConnectionField(ContactType)
    # contact query to return one contact and takes (uid) argument
    # uid is the original object.id in db
    contact = graphene.Field(ContactType, uid=graphene.String())

    def resolve_contact(self, context, uid):
        return ContactType.get_query(context).filter_by(id=uid).first()

    class Meta:
        interfaces = (relay.Node,)


class CreateContact(graphene.Mutation):
    class Arguments:
        """
            Mutation Arguments        
        """
        firstname = graphene.String(required=True)
        lastname = graphene.String()
        description = graphene.String()
        telegram = graphene.String()
        bio = graphene.String()
        emails = graphene.String(required=True)
        telephones = graphene.String(required=True)
        belief_statement = graphene.String()
        owner_id = graphene.String()
        owner_id = graphene.String()
        ownerbackup_id = graphene.String()
        parent_id = graphene.String()
        tf_app = graphene.Boolean()
        tf_web = graphene.Boolean()
        street_number = graphene.Int()

    # MUTATION RESULTS FIELDS
    contact = graphene.Field(ContactType)
    ok = graphene.Boolean()
    errors = graphene.String()

    @classmethod
    def mutate(cls, root, context, **kwargs):
        """ 
        Mutation logic is handled here
        """
        contact = Contact(**kwargs)
        db.session.add(contact)
        try:
            db.session.commit()
            return CreateContact(
                contact=contact,
                ok=True,
                errors=None
            )
        except Exception as e:
            return CreateContact(
                contact=contact,
                ok=False,
                errors=e.args
            )


class ContactMutation(BaseMutation):
    """
    Put all contact mutations here
    """
    create_contact = CreateContact.Field()
