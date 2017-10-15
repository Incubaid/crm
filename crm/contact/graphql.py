import uuid

import graphene
from graphene import relay
from graphene.types.inputobjecttype import InputObjectType

from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql.error.base import GraphQLError

from crm.address.models import Address
from crm.graphql import BaseMutation, BaseQuery, CRMConnectionField
from .models import Contact, Subgroup
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


class AddressArguments(InputObjectType):
    street_number = graphene.String()
    street_name = graphene.String()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    zip_code = graphene.String()


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


class CreateContactArguments(InputObjectType):
    firstname = graphene.String(required=True)
    lastname = graphene.String()
    description = graphene.String()
    telegram = graphene.String()
    bio = graphene.String()
    emails = graphene.String(required=True)
    telephones = graphene.String(required=True)
    belief_statement = graphene.String()
    owner_id = graphene.String()
    ownerbackup_id = graphene.String()
    parent_id = graphene.String()
    tf_app = graphene.Boolean()
    tf_web = graphene.Boolean()
    country = graphene.String()
    message_channels = graphene.String()
    sub_groups = graphene.List(graphene.String)
    addresses = graphene.List(AddressArguments)



class UpdateContactContactArguments(CreateContactArguments):
    uid = graphene.String(required=True)
    firstname = graphene.String()
    emails = graphene.String()
    telephones = graphene.String()


class CreateContacts(graphene.Mutation):
    class Arguments:
        """
            Mutation Arguments        
        """
        records = graphene.List(CreateContactArguments, required=True)

    ok = graphene.Boolean()
    ids = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, context, **kwargs):
        """
        Mutation logic is handled here
        """

        # 'before_insert' hooks won't work with db.session.bulk_save_objects
        # we need to find a way to get hooks to work with bulk_save_objects @todo
        objs = []

        for data in kwargs.get('records', []):
            addresses = data.pop('addresses') if 'addresses' in data else []
            subgroups = data.pop('sub_groups') if 'sub_groups' in data else []

            c = Contact(**data)

            for address in addresses:
                a = Address(**address)
                # Accessing uid once, then it's cached
                # Before insert hook will use the same value
                # So we have same id after insert
                # Reason we access c.uid is that c.id is not available
                # until session.commit()
                a.contact_id = c.uid
                db.session.add(a)

            for subgroup in subgroups:
                pass

            db.session.add(c)

        try:
            db.session.commit()

            return cls(ok=True, ids=[obj.id for obj in objs])
        except Exception as e:
            raise GraphQLError(e.args)


class UpdateContacts(graphene.Mutation):
    class Arguments:
        """
            Mutation Arguments        
        """
        records = graphene.List(UpdateContactContactArguments, required=True)

    ok = graphene.Boolean()
    ids = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, context, **kwargs):
        """
        Mutation logic is handled here
        """

        # 'before_insert' hooks won't work with db.session.bulk_save_objects
        # we need to find a way to get hooks to work with bulk_save_objects @todo

        records = kwargs.get('records', [])
        for data in records:
            data['id'] = data.pop('uid')

        try:
            db.session.bulk_update_mappings(Contact, records)
            db.session.commit()
            return cls(ok=True, ids=[record['id'] for record in records])
        except Exception as e:
            raise GraphQLError(e.args)


class DeleteContacts(graphene.Mutation):
    class Arguments:
        """
            Mutation Arguments        
        """
        uids = graphene.List(graphene.String, required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, context, **kwargs):
        """ 
        Mutation logic is handled here
        """

        # More details about synchronize_session options in SqlAlchemy
        # http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.delete
        Contact.query.filter(
            Contact.id.in_(kwargs.get('uids', []))
        ).delete(synchronize_session=False)

        try:
            db.session.commit()
            return cls(ok=True)

        except Exception as e:
            raise GraphQLError(e.args)


class ContactMutation(BaseMutation):
    """
    Put all contact mutations here
    """
    create_contacts = CreateContacts.Field()
    delete_contacts = DeleteContacts.Field()
    update_contacts = UpdateContacts.Field()
