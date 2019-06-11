import datetime
import factory
import factory.fuzzy
from factory.compat import UTC

from django.conf import settings
from django.contrib.auth.models import User

from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class ExchangeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Exchange

    id_name = factory.Sequence(lambda n: 'Exchange{0}'.format(n))
    active = False


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Account

    apiKey = 'API_KEY'
    secret = 'U0VDUkVUX0NPREU='  # SECRET_CODE Encode to Base64 format
    uid = factory.SubFactory(UserFactory)
    exchange = factory.SubFactory(ExchangeFactory)


class MarketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Market

    exchange = factory.SubFactory(ExchangeFactory)


class MarketOHLCVFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MarketOHLCV

    market = factory.SubFactory(MarketFactory)
    date = factory.fuzzy.FuzzyDateTime(start_dt=datetime.datetime(2008, 1, 1, tzinfo=UTC))
    open = factory.fuzzy.FuzzyFloat(500, 10000)
    hight = factory.fuzzy.FuzzyFloat(500, 10000)
    low = factory.fuzzy.FuzzyFloat(500, 10000)
    close = factory.fuzzy.FuzzyFloat(500, 10000)
    volume = factory.fuzzy.FuzzyFloat(1, 300)


def simulate_fetch_ohlcv():
    import csv
    ohlcv = []
    with open(settings.APPS_DIR.path('exchanges/extras/ohlcv_history'), 'r') as file:
        csv_render = csv.reader(file, delimiter=',')
        for row in csv_render:
            row[0] = int(row[0])
            row = [float(i) if i != row[0] else i for i in row]
            ohlcv.append(row)

    return ohlcv
