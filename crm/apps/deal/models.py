from enum import Enum
from decimal import Decimal

from crm.db import db, BaseModel, RootModel


class DealState(Enum):
    NEW = 'NEW'
    INTERESTED = 'INTERESTED'
    CONFIRMED = 'CONFIRMED'
    CREATED = 'CREATED'
    SIGNED = 'SIGNED'
    PAID = 'PAID'
    CLOSED = 'CLOSED'
    LOST = 'LOST'


DealState.__str__ = lambda self: self.name


class DealType(Enum):
    FARMER = 'FARMER'
    HOSTER = 'HOSTER'
    ITO = 'ITO'
    PTO = 'PTO'
    AMBASSADOR = 'AMBASSADOR'
    ITFT = 'ITFT'
    PREPTO = 'PREPTO'
    TFT = 'TFT'


DealType.__str__ = lambda self: self.name


class Deal(db.Model, BaseModel, RootModel):
    __tablename__ = "deals"

    name = db.Column(
        db.String(255),
        nullable=False,
        index=True,
    )

    # should be markdown.
    description = db.Column(
        db.Text(),
        default="",

    )

    value = db.Column(
        db.Float(),
        default=0.0,
        index=True,
        nullable=False

    )

    currency_id = db.Column(
        db.String(5),
        db.ForeignKey("currencies.id"),
        nullable=False,
    )

    deal_type = db.Column(
        db.Enum(DealType),
        default=DealType.HOSTER,
        index=True,
        nullable=False
    )

    migrated = db.Column(
        db.Boolean()
    )

    deal_state = db.Column(
        db.Enum(DealState),
        default=DealState.NEW,
        index=True,
        nullable=False
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
        db.ForeignKey("contacts.id"),
        index=True
    )

    referrer1_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )



    referrer1 = db.relationship(
        "Contact",
        backref="referrer1_deals",
        foreign_keys=[referrer1_id]
    )

    owner_id = db.Column(
        db.String(5),
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
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

    @property
    def notification_emails(self):
        """
        :return: list of all emails to send notifications to
        :rtype: list
        """
        if self.contact:
            return self.contact.notification_emails
        elif self.company:
            return self.company.notification_emails
        return []

    @property
    def to_usd(self):
        return round(Decimal(self.value) * Decimal(self.currency.value_usd), 2) if self.value else Decimal(0.0)

    @property
    def value_usd(self):
        return '%s' % str(self.to_usd)


    def __str__(self):
            return self.name
