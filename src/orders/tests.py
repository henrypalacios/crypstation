from django.test import TestCase

from src.exchanges.factories import ExchangeFactory, MarketFactory
from src.orders.models import AlertTrade


class AlertTradeTest(TestCase):
    def setUp(self):
        self.kraken = ExchangeFactory.create(id_name='kraken')
        self.market = MarketFactory.create(symbol='BTC/USD', exchange=self.kraken)

    def test_create_new_alert(self):
        alert = {'market': 'BTC/USD', 'side': 'buy', 'price': 8200}

        a = AlertTrade.objects.create(symbol_market=alert['market'], order_type=alert['side'], price=alert['price'])

        self.assertIsInstance(a, AlertTrade)


class TestSignal(TestCase):
    def test_order_is_execute(self):
        alert = {'market': 'BTC/USD', 'side': 'buy', 'price': 8200}
        a = AlertTrade(symbol_market=alert['market'], order_type=alert['side'], price=alert['price'])

        with self.assertLogs("src.orders", level="INFO") as cm:
            a.save()

        self.assertIsInstance(a, AlertTrade)

