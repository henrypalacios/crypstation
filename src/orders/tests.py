from unittest import mock

from django.core import mail
from django.test import TestCase

from src.exchanges.factories import ExchangeFactory, MarketFactory, AccountFactory
from src.orders.factories import AlertTradeFactory
from src.orders.models import AlertTrade, Order


class TestSignal(TestCase):
    def test_order_is_execute(self):
        alert = {'market': 'BTC/USD', 'side': 'buy', 'price': 8200}
        a = AlertTrade(symbol_market=alert['market'], order_type=alert['side'], price=alert['price'])

        with self.assertLogs("src.orders", level="INFO") as cm:
            a.save()

        self.assertIsInstance(a, AlertTrade)


class AutomaticTrader(TestCase):
    def setUp(self):
        self.kraken = ExchangeFactory.create(id_name='kraken')
        self.market = MarketFactory.create(symbol='BTC/USD', exchange=self.kraken)

    def test_execute_order(self):
        AlertTradeFactory.create(symbol_market='btc/usd', order_type='buy', price=100)

        exit('no')
        # execute_order


class AlertTradeTest(TestCase):
    def setUp(self):
        self.kraken = ExchangeFactory.create(id_name='kraken')
        self.market = MarketFactory.create(symbol='BTC/USD', exchange=self.kraken)

    def test_create_new_alert(self):
        alert = {'market': 'BTC/USD', 'side': 'buy', 'price': 8200}

        a = AlertTrade.objects.create(symbol_market=alert['market'], order_type=alert['side'], price=alert['price'])

        self.assertIsInstance(a, AlertTrade)


class OrderTest(TestCase):
    def setUp(self):
        self.kraken = ExchangeFactory.create(id_name='kraken', name='Kraken')
        self.market = MarketFactory.create(symbol='BTC/USD', exchange=self.kraken)

    @mock.patch('ccxt.kraken.create_order')
    def test_create_order(self, MockAPI):
        account = AccountFactory.create(exchange=self.kraken)
        id_order = 'ODZGVT-BPBYV-X64OTL'
        MockAPI.return_value = {'id': 'ODZGVT-BPBYV-X64OTL',
                                'info': {
                                    'error': [],
                                    'result': {'descr':
                                                   {'order': 'buy 0.10000000 XBTUSD @ limit 7000.0'},
                                               'txid': ['ODZGVT-BPBYV-X64OTL']}
                                },
                                'timestamp': None,
                                'datetime': None,
                                'lastTradeTimestamp': None,
                                'symbol': 'BTC/USD',
                                'type': 'limit',
                                'side': 'buy',
                                'price': 7000,
                                'amount': 0.1,
                                'cost': None,
                                'average': None,
                                'filled': None,
                                'remaining': None,
                                'status': None,
                                'fee': None,
                                'trades': None}

        Order.objects.put_order_in_exchange(account, self.market, 'buy', '7000', 0.1, "TestTrade[123]")

        self.assertEquals(id_order, Order.objects.first().id_order)

    @mock.patch('ccxt.kraken.create_order')
    def test_create_order_sends_email(self, MockAPI):
        #TODO
        account = AccountFactory.create(exchange=self.kraken)
        id_order = 'ODZGVT-BPBYV-X64OTL'
        MockAPI.return_value = {'id': id_order}

        with self.assertLogs('src.orders.tasks', level='INFO') as cm:
            Order.objects.put_order_in_exchange(account, self.market, 'buy', '7000', 0.1, "TestTrade[123]")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Crypstation')
        #self.assertGreaterEqual(len(cm.output), 1)