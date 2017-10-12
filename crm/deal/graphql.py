import graphene
from graphene import relay
from graphene.types.inputobjecttype import InputObjectType

from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql.error.base import GraphQLError

from crm.graphql import BaseMutation, BaseQuery, CRMConnectionField
from .models import Deal
from crm import db


class DealType(SQLAlchemyObjectType):
    # object.id in graphene contains internal
    # representation of id.
    # we add another uid field that we fill
    # with original object.id
    uid = graphene.String()

    class Meta:
        model = Deal
        interfaces = (relay.Node,)
        name = model.__name__


class DealQuery(BaseQuery):
    """
    we have 2 queries here Deal and Deals
    """

    # no need for resplve_Deals function here
    deals = CRMConnectionField(DealType)
    # Deal query to return one Deal and takes (uid) argument
    # uid is the original object.id in db
    deal = graphene.Field(DealType, uid=graphene.String())

    def resolve_deal(self, context, uid):
        return DealType.get_query(context).filter_by(id=uid).first()

    class Meta:
        interfaces = (relay.Node,)


class CreateDealArguments(InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    amount = graphene.Float()
    currency = graphene.String(required=True)
    deal_type = graphene.String(required=True)
    deal_state = graphene.String(required=True)
    closed_at = graphene.String()
    company_id = graphene.String()
    contact_id = graphene.String()
    referral_code = graphene.String()


class UpdateDealArguments(CreateDealArguments):
    uid = graphene.String(required=True)
    name = graphene.String()
    currency = graphene.String()
    deal_type = graphene.String()
    deal_state = graphene.String()


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
            c = Deal(**data)
            db.session.add(c)
            objs.append(c)
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

        records = kwargs.get('records', [])
        for data in records:
            data['id'] = data.pop('uid')

        try:
            db.session.bulk_update_mappings(Deal, records)
            db.session.commit()
            return cls(ok=True, ids=[record['id'] for record in records])
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
        Deal.query.filter(
            Deal.id.in_(kwargs.get('uids', []))
        ).delete(synchronize_session=False)

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



