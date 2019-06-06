from django.db import models

from src.exchanges.models import Market


class AllowedTradeManager(models.Manager):
    def fire_order(self, market, price, side):
        market = Market.objects.get(symbol=market)
        traders = self.filter(market=market)

        for trader in traders:
            market.create_order(trader.account, side, price)


class AllowedTrade(models.Model):
    account = models.ForeignKey('Account', related_name='allowed_trades', on_delete=models.CASCADE)
    market = models.ForeignKey('Market', related_name='accounts', on_delete=models.CASCADE)

    objects = AllowedTradeManager()

