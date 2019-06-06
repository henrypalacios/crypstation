import ccxt
import datetime
import pytz

from django.db import models
from django.contrib.auth.models import User

from src.exchanges.managers import MarketOHLCVManager, MarketManager


class Exchange(models.Model):
    id_name = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    @property
    def instance(self, params={}):
        return eval('ccxt.%s(%s)' % (self.id_name, params))

    def get_markets(self):
        return self.instance.load_markets()


class Account(models.Model):
    apiKey = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True)
    uid = models.OneToOneField(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey('Exchange', related_name='account', on_delete=models.CASCADE)

    def set_apikey(self, instance_api):
        instance_api.apiKey = self.apiKey
        instance_api.secret = self.secret

        return instance_api


class Market(models.Model):
    symbol = models.CharField(max_length=50, db_index=True)
    exchange = models.ForeignKey('Exchange', related_name='markets', on_delete=models.CASCADE)
    data = models.TextField()

    objects = MarketManager()

    FROM_DATE = datetime.datetime(2018, 1, 1, tzinfo=pytz.utc)

    @property
    def exchange_api(self):
        return self.exchange.instance

    def fetch_ohlcv_history(self, timeframe='1m', from_datetime=None, from_timestamp=None, limit=500):
        ex_api = self.exchange_api

        if from_datetime:
            from_timestamp = self.conver_datetime_to_timestamp(ex_api, from_datetime)
        elif not from_timestamp:
            raise ValueError('It\'s necessary specified: from_datetime or from_timestamp')

        ohlcvs = ex_api.fetch_ohlcv(self.symbol, timeframe, since=from_timestamp, limit=limit)

        return ohlcvs

    def conver_datetime_to_timestamp(self, exchange_api: ccxt.Exchange, datetime):
        return exchange_api.parse8601(datetime)

    def create_order(self, account: Account, side, price, type_order='market', amount=None, params={}):
        exchange_api = account.set_apikey(self.exchange_api)

        order = exchange_api.create_order(self.symbol, type_order, side, amount, price, params)

        return order


class MarketOHLCV(models.Model):
    """ For default represent the time frame the 1 minute"""

    market = models.ForeignKey('Market', related_name='ohlcv', on_delete=models.CASCADE)
    date = models.DateTimeField()
    open = models.FloatField()
    hight = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()

    objects = MarketOHLCVManager()
