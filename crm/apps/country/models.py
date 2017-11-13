from crm.db import db, BaseModel

from .countries import CountriesEnum


class Country(db.Model, BaseModel):

    __tablename__ = "countries"

    name = db.Column(
        db.Enum(CountriesEnum),
        default=CountriesEnum.BE,
        unique=True,
        index=True
    )

    contacts = db.relationship(
        "Contact",
        secondary="contacts_countries",
        backref="countries"
    )

    addresses = db.relationship(
        "Address",
        backref="country"
    )

    passports = db.relationship(
        "Passport",
        backref="country"
    )

    def __str__(self):
        return self.name.value