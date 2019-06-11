import datetime
import ccxt
import pytz
from unittest import mock

from django.test import TestCase
from django.core.management import call_command

from .utils import parse_datetime
from . import factories as factory
from .factories import ExchangeFactory, MarketFactory, MarketOHLCVFactory, AccountFactory
from .models import Market, Exchange, MarketOHLCV


class ExchangeTest(TestCase):
    def setUp(self):
        self.kraken = ExchangeFactory.create(id_name='kraken')
        self.market = MarketFactory.create(symbol='BTC/USD', exchange=self.kraken)

    def test_get_api_instance(self):
        api = self.kraken.api_instance()

        self.assertIsInstance(api, ccxt.Exchange)

    def test_get_api_instance_with_parameters(self):
        api_key = 'KEY'
        secret = 'CODE'
        rate_limit = True
        api = self.kraken.api_instance({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': rate_limit,
        })

        self.assertEquals(api.apiKey, api_key)
        self.assertEquals(api.secret, secret)
        self.assertEquals(api.enableRateLimit, rate_limit)


class MarketTest(TestCase):
    def setUp(self):
        self.kraken = ExchangeFactory.create(id_name='kraken')
        self.market = MarketFactory.create(symbol='BTC/USD', exchange=self.kraken)

    @mock.patch('ccxt.kraken.fetch_ohlcv')
    def test_fecth_ohlcv(self, FecthMock):
        datetime = '2017-01-01 00:00:00'
        FecthMock.return_value = factory.simulate_fetch_ohlcv()

        ohlcv = self.market.fetch_ohlcv_history(from_datetime=datetime)

        self.assertEqual(720, len(ohlcv))

    def test_convert_datetime_to_timestamp(self):
        kraken = self.kraken
        market = self.market
        datetime = '2015-01-01 00:00:00'
        expected_timestamp = 1420070400000

        timestamp = market.convert_datetime_to_timestamp(market.exchange_api(), datetime)

        self.assertEqual(expected_timestamp, timestamp)

    def test_get_last_historical_date(self):
        first_timestamp = 1546300800000  # 2019-01-01 00:00:00
        last_timestamp = 1546301100000  # 2019-01-01 00:05:00
        lure_timestamp = 1557032705000  # 2019-05-05 05:05:05
        last_date = parse_datetime(last_timestamp)
        MarketOHLCVFactory.create(market=self.market, date=parse_datetime(first_timestamp))
        MarketOHLCVFactory.create(market=self.market, date=last_date)
        # The Lure Row
        MarketOHLCVFactory.create(date=parse_datetime(lure_timestamp))

        date = Market.objects.get_last_historical_date(self.market)

        self.assertEqual(last_date, date)
        self.assertIsInstance(date, datetime.datetime)

    def test_get_last_historical_date_when_not_exists_ohlcv_in_market(self):
        lure_timestamp = 1557032705000  # 2019-05-05 05:05:05
        # The Lure Row
        MarketOHLCVFactory.create(date=parse_datetime(lure_timestamp))

        result = Market.objects.get_last_historical_date(self.market)

        self.assertEqual(Market.FROM_DATE, result)
        self.assertIsInstance(result, datetime.datetime)


class MarketOHLCVTest(TestCase):
    def setUp(self):
        self.kraken = ExchangeFactory.create(id_name='kraken')
        self.market = MarketFactory.create(symbol='BTC/USD', exchange=self.kraken)
        self.raw_ohlcv = [[1546300800000, 3698.0, 3700.6, 3697.9, 3700.6, 5.0886],
                          [1546300860000, 3700.6, 3709.9, 3700.6, 3709.8, 7.15316174]]

    def test_build_from_ohlcv(self):
        lot_ohlcv = factory.simulate_fetch_ohlcv()

        saved = MarketOHLCV.objects.bulk_ohlcv(market=self.market, ohlcv=lot_ohlcv)

        self.assertEqual(720, saved)
        self.assertEqual(720, MarketOHLCV.objects.count())

    def test_add_price(self):
        date = datetime.datetime(2019, 1, 1, hour=0, minute=1, second=0, tzinfo=pytz.utc)

        MarketOHLCV.objects.add_price(self.market, self.raw_ohlcv)

        self.assertEqual(2, MarketOHLCV.objects.count())
        self.assertEqual(date, MarketOHLCV.objects.last().date)


class UtilsTest(TestCase):
    def test_parse_datetime(self):
        """Parse keeping utc.

        Note: unix_time parameters for default it's received in milliseconds"""

        from .utils import parse_datetime
        unix_time = 1546300800000
        date = datetime.datetime(2019, 1, 1, tzinfo=pytz.utc)

        parse = parse_datetime(unix_time)

        self.assertEqual(date, parse)

    def test_parse_datetime_when_unit_time_parameters_not_has_milliseconds(self):
        from .utils import parse_datetime
        unix_time = 1546300800
        date = datetime.datetime(2019, 1, 1, tzinfo=pytz.utc)

        parse = parse_datetime(unix_time, has_milliseconds=False)

        self.assertEqual(date, parse)


class AccountTest(TestCase):
    def setUp(self):
        self.kraken = ExchangeFactory.create(id_name='kraken')
        self.market = MarketFactory.create(symbol='BTC/USD', exchange=self.kraken)

    @mock.patch('src.exchanges.models.Market.exchange_api')
    def test_put_order_exchange(self, MockExchangeApi):
        account = AccountFactory.create(exchange=self.kraken)
        order_id = 123
        MockExchangeApi.return_value.create_order.return_value = order_id


        order = account.put_order_exchange(self.market, side='buy', price=800, amount=100, type_order='market',
                                           params={'test': True})

        self.assertEquals(order_id, order)
