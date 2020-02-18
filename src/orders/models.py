from django.db import models

from src.exchanges.models import Market, Account


class AutomaticTraderManager(models.Manager):
    def execute_order(self, alert_trade: 'AlertTrade'):
        traders = self.filter(market=alert_trade.symbol_market)

        for trader in traders:
            amount = eval(self.trader.AMOUNT_CHOICES[alert_trade.order_side])
            Order.objects.create_order(trader.account, trader.market, alert_trade.order_side, alert_trade.price,
                                       amount, f'AlertTrade[{alert_trade.pk}]')


class AutomaticTrader(models.Model):
    AMOUNT_CHOICES = {
        'sell': 'first_pair_amount',
        'buy': 'second_pair_amount'
    }

    account = models.ForeignKey(Account, related_name='automatic_trades', on_delete=models.CASCADE)
    market = models.ForeignKey(Market, related_name='automatic_trades', on_delete=models.CASCADE)
    first_pair_amount = models.FloatField()
    second_pair_amount = models.FloatField()
    active = models.BooleanField(default=True)

    objects = AutomaticTraderManager()


class AlertTrade(models.Model):
    ORDERS = (
        ('buy', 'BUY'),
        ('sell', 'SELL')
    )

    symbol_market = models.CharField(max_length=10)
    order_side = models.CharField(max_length=10, choices=ORDERS)
    price = models.FloatField()
    strategy = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    automatically_executed = models.BooleanField(default=False)


class OrderManager(models.Manager):
    def put_order_in_exchange(self, account, market, side, price, amount, reference):
        from src.orders.tasks import send_notification

        api_exchange = account.get_private_instance()
        try:
            # print(f".create_order({market.symbol}, 'limit', {side}, {amount}, {price})")
            response = api_exchange.create_order(market.symbol, 'limit', side, amount, price)

        except Exception as e:
            raise Exception('Failed to create order with', api_exchange.id, type(e).__name__, str(e))

        self.create(id_order=response['id'], account=account, market=market, order_side=side,
                    quantity=amount, price=price)

        send_notification.delay(account.uid.email, side, f'{market.exchange.name}-{market.symbol}', price, amount)


class Order(models.Model):
    id_order = models.CharField(max_length=250)
    account = models.ForeignKey(Account, related_name='account_orders', on_delete=models.CASCADE)
    market = models.ForeignKey(Market, related_name='market_orders', on_delete=models.CASCADE)
    order_side = models.CharField(max_length=10)
    quantity = models.FloatField()
    price = models.FloatField()

    objects = OrderManager()
