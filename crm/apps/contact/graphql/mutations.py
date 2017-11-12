import graphene
from graphql.error.base import GraphQLError
from sqlalchemy.inspection import inspect

from crm import db
from crm.apps.contact.models import Contact
from crm.graphql import BaseMutation
from .arguments import CreateContactArguments, UpdateContactArguments


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
            c = Contact.get_object_from_graphql_input(data)
            db.session.add(c)
            objs.append(c)
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
        records = graphene.List(UpdateContactArguments, required=True)

    ok = graphene.Boolean()
    ids = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, context, **kwargs):
        """
        Mutation logic is handled here
        """

        # 'before_insert' hooks won't work with db.session.bulk_save_objects
        # we need to find a way to get hooks to work with bulk_save_objects @todo

        records = []
        for data in kwargs.get('records', []):
            actual = Contact.query.get(data['uid'])

            if not actual:
                raise GraphQLError('Invalid id (%s)' % data['id'])

            c = Contact.get_object_from_graphql_input(data)

            for column_name, _ in inspect(Contact).attrs.items():
                if column_name == 'id':
                    continue
                if column_name not in data:
                    continue
                setattr(actual, column_name, getattr(c, column_name))
            db.session.add(actual)
            records.append(actual.id)
        try:
            db.session.commit()
            return cls(ok=True, ids=records)
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
