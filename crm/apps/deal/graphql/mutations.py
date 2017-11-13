import graphene
from graphql.error.base import GraphQLError
from sqlalchemy.inspection import inspect

from crm import db
from crm.graphql import BaseMutation
from .arguments import CreateDealArguments, UpdateDealArguments
from crm.apps.deal.models import Deal


class CreateDeals(graphene.Mutation):
    class Arguments:
        """
            Mutation Arguments        
        """
        records = graphene.List(CreateDealArguments, required=True)

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
            d = Deal.get_object_from_graphql_input(data)
            db.session.add(d)
            objs.append(d)
        try:
            db.session.commit()
            return cls(ok=True, ids=[obj.id for obj in objs])
        except Exception as e:
            raise GraphQLError(e.args)


class UpdateDeals(graphene.Mutation):
    class Arguments:
        """
            Mutation Arguments        
        """
        records = graphene.List(UpdateDealArguments, required=True)

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
            actual = Deal.query.get(data['uid'])

            if not actual:
                raise GraphQLError('Invalid id (%s)' % data['id'])

            d = Deal.get_object_from_graphql_input(data)

            for column_name, _ in inspect(Deal).attrs.items():
                if column_name == 'id':
                    continue
                if column_name not in data:
                    continue
                setattr(actual, column_name, getattr(d, column_name))
            db.session.add(actual)
            records.append(actual.id)
        try:
            db.session.commit()
            return cls(ok=True, ids=records)
        except Exception as e:
            raise GraphQLError(e.args)


class DeleteDeals(graphene.Mutation):
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

        query = Deal.query.filter(
            Deal.id.in_(kwargs.get('uids', [])))

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


class DealMutation(BaseMutation):
    """
    Put all Deal mutations here
    """
    create_deals = CreateDeals.Field()
    delete_deals = DeleteDeals.Field()
    update_deals = UpdateDeals.Field()
