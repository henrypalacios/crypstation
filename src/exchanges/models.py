import ccxt
import datetime
import pytz

from django.db import models
from django.contrib.auth.models import User
from django.forms import PasswordInput

from src.exchanges.managers import MarketOHLCVManager, MarketManager


class Exchange(models.Model):
    id_name = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return f'{self.id_name}[{self.pk}]'

    def api_instance(self, params={}):
        return eval('ccxt.%s(%s)' % (self.id_name, params))

    def get_markets(self):
        return self.api_instance().load_markets()


class Account(models.Model):
    apiKey = models.CharField(max_length=255, widget=PasswordInput)
    secret = models.CharField(max_length=255, widget=PasswordInput)
    password = models.CharField(max_length=255, null=True, blank=True, widget=PasswordInput)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey('Exchange', related_name='account', on_delete=models.CASCADE)

    def __str__(self):
        return '%s-%s' % (self.uid, self.exchange.id_name)

    def get_private_instance(self):
        api_exchange = self.exchange.api_instance({'apiKey': self.apiKey, 'secret': self.secret})

        return api_exchange

    # @classmethod
    # def private_instance_api(self, user_id, exchange_name):
    #
    #     return instance_api

    def put_order_exchange(self, market: 'Market', side, price, amount, type_order='market', params={}):
        exchange_api = market.exchange_api(self.apiKey, self.secret)

        order = exchange_api.create_order(market.symbol, type_order, side, amount, price, params)

        return order


class Market(models.Model):
    symbol = models.CharField(max_length=50, db_index=True)
    exchange = models.ForeignKey('Exchange', related_name='markets', on_delete=models.CASCADE)
    data = models.TextField()

    objects = MarketManager()

    FROM_DATE = datetime.datetime(2018, 1, 1, tzinfo=pytz.utc)

    def __str__(self):
        return '%s-%s' % (self.exchange.id_name, self.symbol)

    def exchange_api(self, api_key=None, secret=None):
        params = {}
        if api_key:
            params.update({'apiKey': api_key})
            params.update({'secret': secret})

        return self.exchange.api_instance(params)

    def fetch_ohlcv_history(self, timeframe='1m', from_datetime=None, from_timestamp=None, limit=500):
        ex_api = self.exchange_api()

        if from_datetime:
            from_timestamp = self.convert_datetime_to_timestamp(ex_api, from_datetime)
        elif not from_timestamp:
            raise ValueError('It\'s necessary specified: from_datetime or from_timestamp')

        ohlcvs = ex_api.fetch_ohlcv(self.symbol, timeframe, since=from_timestamp, limit=limit)

        return ohlcvs

    def convert_datetime_to_timestamp(self, exchange_api: ccxt.Exchange, datetime):
        return exchange_api.parse8601(datetime)


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
