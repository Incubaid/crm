import graphene
from graphene import relay

from crm.apps.country.graphql.arguments import CountryArguments
from crm.apps.country.graphql.types import CountryType
from crm.graphql import BaseQuery, CRMConnectionField


class CountryQuery(BaseQuery):
    countries = CRMConnectionField(
        CountryType,
        **CountryArguments.fields()
    )

    country = graphene.Field(CountryType, uid=graphene.String())

    def resolve_country(self, context, uid):
        return CountryType.get_query(context).filter_by(id=uid).first()


    class Meta:
        interfaces = (relay.Node, )