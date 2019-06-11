from django.db import models

from src.exchanges.models import Market, Account


class AutomaticTraderManager(models.Manager):
    def fire_order(self, market, price, side):
        market = Market.objects.get(symbol=market)
        traders = self.filter(market=market)

        for trader in traders:
            market.put_order_exchange(trader.account, side, price)


class AutomaticTrader(models.Model):
    AMOUNT_CHOICES = {
        'sell': 'first_pair_amount',
        'buy': 'second_pair_amount'
    }

    account = models.ForeignKey(Account, related_name='allowed_trades', on_delete=models.CASCADE)
    market = models.ForeignKey(Market, related_name='accounts', on_delete=models.CASCADE)
    first_pair_amount = models.FloatField()
    second_pair_amount = models.FloatField()

    objects = AutomaticTraderManager()

