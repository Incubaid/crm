import graphene
from graphql.error.base import GraphQLError

from crm import db
from crm.apps.address.models import Address
from crm.apps.contact.models import Contact, Subgroup
from crm.graphql import BaseMutation
from .arguments import CreateContactArguments, UpdateContactContactArguments


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
        records = kwargs.get('records', [])
        objs = []
        for data in records:
            addresses = data.pop('addresses') if 'addresses' in data else []
            subgroups = data.pop('sub_groups') if 'sub_groups' in data else []
            c = Contact(**data)
            c.addresses = [ Address(**address) for address in addresses]
            c.subgroups = [Subgroup(groupname=subgroup) for subgroup in subgroups]
            # db.session.add(c)
            c.update_auto_fields()
            objs.append(c)
        try:
            db.session.info['changes'] = {'created': objs, 'updated': [], 'deleted':{}}
            db.session.bulk_save_objects(objs)
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
            addresses = data.pop('addresses') if 'addresses' in data else []
            subgroups = data.pop('sub_groups') if 'sub_groups' in data else []
            c = Contact.query.filter_by(id=data['id']).first()

            if not c:
                raise GraphQLError('Invalid id (%s)' % data['id'])

            for k, v in data.items():
                setattr(c, k, v)

            if addresses:
                c.addresses = [Address(**address) for address in addresses]
            if subgroups:
                c.subgroups = [Subgroup(groupname=subgroup) for subgroup in subgroups]
            db.session.add(c)
        try:
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

        query = Contact.query.filter(
            Contact.id.in_(kwargs.get('uids', [])))

        objs = []

        for obj in query:
            db.session.delete(obj)
            objs.append(obj)

        db.session.info['changes'] = {'created': [], 'updated': [], 'deleted': objs}
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
