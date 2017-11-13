from crm import db
from crm.db import BaseModel, RootModel


class Currency(db.Model, BaseModel, RootModel):

    __tablename__ = "currencies"

    name = db.Column(
        db.String(3),
        index=True,
        unique=True,
        nullable=False,
    )

    value_usd = db.Column(
        db.Float(),
        default=1.0
    )

    deals = db.relationship(
        "Deal",
        backref="currency"
    )

    def __str__(self):
        return self.name
