import graphene
from graphene import relay
from decimal import Decimal

from crm.apps.deal.graphql.arguments import DealArguments
from crm.apps.deal.graphql.types import OverAllDealStatsType, DealsStatsType
from crm.apps.fund.models import FundRound
from .types import DealType
from crm.graphql import BaseQuery, CRMConnectionField
from crm.apps.deal.models import DealType as DealTypeEnum
from crm.apps.deal.models import DealState as DealStateEnum


class DealQuery(BaseQuery):
    """
    we have 2 queries here Deal and Deals
    """

    # no need for resplve_Deals function here
    deals = CRMConnectionField(
        DealType,
        DealArguments.fields()

    )

    # Deal query to return one Deal and takes (uid) argument
    # uid is the original object.id in db
    deal = graphene.Field(DealType, uid=graphene.String())
    deals_stats = graphene.Field(OverAllDealStatsType)

    def resolve_deal(self, context, uid):
        return DealType.get_query(context).filter_by(id=uid).first()

    @staticmethod
    def _get_stats(round):
        stats = {
            'start': None,
            'end': None,
            'total': Decimal(0.0),
            'new': Decimal(0.0),
            'interested': Decimal(0.0),
            'confirmed': Decimal(0.0),
            'lost': Decimal(0.0),
            'created': Decimal(0.0),
            'signed': Decimal(0.0),
            'paid': Decimal(0.0),
            'closed': Decimal(0.0),
            'hoster': Decimal(0.0),
            'ito': Decimal(0.0),
            'pto': Decimal(0.0),
            'ambassador': Decimal(0.0),
            'itft': Decimal(0.0),
            'prepto': Decimal(0.0),
            'target': Decimal(0.0)
        }

        if round:
            stats['start'] = round.start
            stats['end'] = round.end
            stats['target'] = round.target

            for deal in round.deals:
                stats['total'] += deal.to_usd
                if deal.deal_type == DealTypeEnum.AMBASSADOR:
                    stats['ambassador'] += deal.to_usd
                elif deal.deal_type == DealTypeEnum.HOSTER:
                    stats['hoster'] += deal.to_usd
                elif deal.deal_type == DealTypeEnum.ITFT:
                    stats['itft'] += deal.to_usd
                elif deal.deal_type == DealTypeEnum.ITO:
                    stats['ito'] += deal.to_usd
                elif deal.deal_type == DealTypeEnum.PREPTO:
                    stats['prepto'] += deal.to_usd
                elif deal.deal_type == DealTypeEnum.PTO:
                    stats['pto'] += deal.to_usd

                if deal.deal_state == DealStateEnum.CLOSED:
                    stats['closed'] += deal.to_usd
                elif deal.deal_state == DealStateEnum.CONFIRMED:
                    stats['confirmed'] += deal.to_usd
                elif deal.deal_state == DealStateEnum.CREATED:
                    stats['created'] += deal.to_usd
                elif deal.deal_state == DealStateEnum.INTERESTED:
                    stats['interested'] += deal.to_usd
                elif deal.deal_state == DealStateEnum.LOST:
                    stats['lost'] += deal.to_usd
                elif deal.deal_state == DealStateEnum.NEW:
                    stats['new'] += deal.to_usd
                elif deal.deal_state == DealStateEnum.PAID:
                    stats['paid'] += deal.to_usd
                elif deal.deal_state == DealStateEnum.SIGNED:
                    stats['signed'] += deal.to_usd
        return stats

    def resolve_deals_stats(self, context):
        curr_round = FundRound.current_round()
        current_round_stats = DealQuery._get_stats(curr_round)

        old_rounds_stats = []
        old_rounds = FundRound.old_rounds()

        for round in old_rounds:
            old_rounds_stats.append(DealQuery._get_stats(round))

        stats = OverAllDealStatsType()
        stats.current_round = DealsStatsType(**current_round_stats)
        stats.old_rounds = [DealsStatsType(**d) for d in old_rounds_stats]
        return stats

    class Meta:
        interfaces = (relay.Node,)
