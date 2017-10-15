import enum
from crm.db import db, BaseModel, RootModel
from crm.countries import countries

CountriesEnum = enum.Enum('Countries', {v: v for k, v in countries.items()})

CountriesEnum.__str__ = lambda self: self.value


class Address(db.Model, BaseModel, RootModel):

    __tablename__ = "addresses"

    street_number = db.Column(
        db.String(255),
    )

    street_name = db.Column(
        db.String(255),
        default=""
    )

    description = db.Column(
        db.Text(),
        default=""
    )

    city = db.Column(
        db.Text(),
        default=""
    )

    state = db.Column(
        db.Text(),
        default=""
    )

    zip_code = db.Column(
        db.String(255)
    )

    country = db.Column(
        db.Enum(CountriesEnum),
        default=CountriesEnum.Belgium
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey('contacts.id')
    )
    company_id = db.Column(
        db.String(5),
        db.ForeignKey('companies.id')
    )
    deal_id = db.Column(
        db.String(5),
        db.ForeignKey('deals.id')
    )

    @property
    def formatted_address(self):
        address = ''
        if self.street_name:
            if self.street_number:
                address += '%s %s, ' % (self.street_number, self.street_name)
            else:
                address += '%s, ' % self.street_name

        if self.state:
            address += '%s, ' % self.state
        if self.city:
            address += '%s, ' % self.city
        if self.country:
            address += str(self.country)

        if self.zip_code:
            address += ' (zip code: %s)' % self.zip_code

        return address

    def __str__(self):
        return self.formatted_address
