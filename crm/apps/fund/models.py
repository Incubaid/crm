from datetime import datetime

from sqlalchemy_utils import InstrumentedList

from crm.apps.deal.models import Deal
from crm.db import db, BaseModel, RootModel


class FundRound(db.Model, BaseModel, RootModel):
    __tablename__ = "fund_rounds"

    title = db.Column(
        db.String(),
        index=True,
        nullable=False
    )

    start = db.Column(
        db.TIMESTAMP,
        nullable=False,
        index=True,
    )

    end = db.Column(
        db.TIMESTAMP,
        nullable=False,
        index=True,
    )

    target = db.Column(
        db.Float(),
        default=0.0,
        index=True,
        nullable=False

    )

    def __str__(self):
        return self.title

    @staticmethod
    def current_round():
        now = datetime.now()
        return FundRound.query.filter(FundRound.end >= now.date()).order_by(FundRound.start.asc()).first()

    @staticmethod
    def old_rounds():
        now = datetime.now()
        return FundRound.query.filter(FundRound.end < now).all()

    @property
    def deals(self):
        q = Deal.query.filter(Deal.closed_at >= self.start, Deal.closed_at <= self.end)
        # return None if no deals, so in details page of round, no deals will be diplayed
        # return InstrumentedList of deals if found so that deals are formatted automatically in nice manner
        # because formatter, does format format actual model fields of type (InstrumentedList) automatically
        # but since this is a property, we do the change to InstrumentedList so we get formatting out of the box
        if q.count():
            return InstrumentedList(q.all())
        return InstrumentedList([])
