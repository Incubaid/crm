from enum import Enum

from crm.db import db, BaseModel, RootModel


class DealState(Enum):
    NEW, INTERESTED, CONFIRMED, PENDING, CLOSED = range(5)


class DealType(Enum):
    HOSTER, ITO, PTO, AMBASSADOR, ITFT = range(5)


class DealCurrency(Enum):
    USD, EUR, AED, GBP, BTC = range(5)


class Deal(db.Model, BaseModel, RootModel):

    __tablename__ = "deals"

    name = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    # should be markdown.
    description = db.Column(
        db.Text(),
        default="",

    )

    amount = db.Column(
        db.Float(),
        index=True

    )

    currency = db.Column(
        db.Enum(DealCurrency),
        default=DealCurrency.EUR,
        index=True
    )

    deal_type = db.Column(
        db.Enum(DealType),
        default=DealType.HOSTER,
        index=True
    )

    deal_state = db.Column(
        db.Enum(DealState),
        default=DealState.NEW,
        index=True
    )

    closed_at = db.Column(
        db.TIMESTAMP,
        nullable=True
    )

    company_id = db.Column(
        db.String(5),
        db.ForeignKey("companies.id")
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )

    referrer1_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )

    referrer2_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )


    referrer1 = db.relationship(
        "Contact",
        backref="referrer1_deals",
        foreign_keys=[referrer1_id]
    )

    referrer2 = db.relationship(
        "Contact",
        backref="referrer2_deals",
        foreign_keys=[referrer2_id]
    ) 
    tasks = db.relationship(
        "Task",
        backref="deal"
    )

    comments = db.relationship(
        "Comment",
        backref="deal"
    )

    messages = db.relationship(
        "Message",
        backref="deal"
    )

    links = db.relationship(
        "Link",
        backref="deal"
    )

    is_paid = db.Column(
        db.Boolean(),
        index=True
    )
    referral_code = db.Column(
        db.String(255),
        index=True
    )

    shipping_address = db.relationship(
        "Address",
        backref="deal"
    )

    def __str__(self):
        return self.name
