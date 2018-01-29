import time
import datetime
import requests

from crm import app
from crm.apps.currency.models import Currency


session = requests.Session()


@app.cli.command()
def update_currency_rates():
    """
    Updates Currencies exchange rates to USD
    """
    while True:
        res = session.get('http://apilayer.net/api/live?access_key=955ebff5d2c404fcfb383b587a02a97b&currencies=AED,GBP,EUR,BTC&format=1')
        if res.status_code != 200:
            print('error getting currency rates : ', res.content)
            time.sleep(21600)
            continue

        res = res.json()['quotes']
        AED = round(1.0/res['USDAED'], 2)
        GBP = round(1.0/res['USDGBP'], 2)
        EUR = round(1.0/res['USDEUR'], 2)
        BTC = round(1.0/res['USDBTC'], 2)


        Currency.query.filter_by(name='AED').update({'value_usd': AED})
        Currency.query.filter_by(name='GBP').update({'value_usd': GBP})
        Currency.query.filter_by(name='EUR').update({'value_usd': EUR})
        Currency.query.filter_by(name='BTC').update({'value_usd': BTC})
        print('Last update : ', datetime.datetime.now())

        print('Now sleeping for 6 hours')
        time.sleep(21600)
