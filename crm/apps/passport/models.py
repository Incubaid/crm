import datetime
import enum
from crm.countries import CountriesEnum
from crm.db import db, BaseModel


class Passport(db.Model, BaseModel):

    __tablename__ = "passports"

    passport_fullname = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    passport_number = db.Column(
        db.Text(),
        index=True
    )

    issuance_date = db.Column(
        db.Date(),
        default=datetime.date(1990, 1, 1),
        nullable=False
    )
    expiration_date = db.Column(
        db.Date(),
        default=datetime.date(2020, 1, 1),
        nullable=False
    )
    country = db.Column(
        db.Enum(CountriesEnum),
        default=CountriesEnum.Belgium,
        index=True
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey('contacts.id')
    )

    def __str__(self):
        return "Passport {}".format(self.passport_fullname)
