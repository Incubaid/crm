from crm import app
from crm.apps.contact.models import SubgroupName, Subgroup
from crm.apps.currency.models import Currency
from crm.db import db
from crm.apps.country.countries import CountriesEnum
from crm.apps.country.models import Country


@app.cli.command()
def load():
    """
    Add missing enum data to tables that use these enums
    i.e contact.countries, contact.subgroups
    """
    for country in CountriesEnum:
        c = Country.query.filter_by(name=country).first()
        if c is not None:
            continue
        c = Country(name=country)
        db.session.add(c)

    for subgroup in SubgroupName:
        s = Subgroup.query.filter_by(groupname=subgroup).first()
        if s is not None:
            continue
        s = Subgroup(groupname=subgroup)
        db.session.add(s)

    for currency in ['USD', 'EUR', 'AED', 'GBP', 'BTC']:
        c = Currency.query.filter_by(name=currency).first()
        if c is not None:
            continue
        c = Currency(name=currency)
        db.session.add(c)
    db.session.commit()