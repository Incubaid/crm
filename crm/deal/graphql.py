import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Deal


class DealType(SQLAlchemyObjectType):

    class Meta:
        model = Deal


class DealQuery(graphene.AbstractType):
    deals = graphene.List(DealType)

    def resolve_deals(self, args, context, info):
        query = DealType.get_query(context)
        return query.all()
