import graphene
from graphene import relay

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
    we have 2 queries here contact and contacts
    """

    # no need for deals function here
    deals = CRMConnectionField(DealType)
    # deal query to return one contact and takes (uid) argument
    # uid is the original object.id in db
    deal = graphene.Field(DealType, uid=graphene.String())

    def resolve_deal(self, context, uid):
        return DealType.get_query(context).filter_by(id=uid).first()

    class Meta:
        interfaces = (relay.Node,)


class CreateDeal(graphene.Mutation):
    class Arguments:
        """
            Mutation Arguments        
        """
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

    # MUTATION RESULTS FIELDS
    deal = graphene.Field(DealType)
    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, context, **kwargs):
        """ 
        Mutation logic is handled here
        """
        deal = Deal(**kwargs)
        db.session.add(deal)
        try:
            db.session.commit()
            return CreateDeal(
                deal=deal,
                ok=True,
                errors = []
            )
        except Exception as e:
            raise GraphQLError(e.args)


class DealMutation(BaseMutation):
    """
    Put all deal mutations here
    """
    create_deal = CreateDeal.Field()
