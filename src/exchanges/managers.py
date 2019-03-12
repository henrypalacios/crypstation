from django.db import models

# from src.exchanges.services import ManagerCCXT
from src.exchanges.utils import parse_datetime


# class ExchangeManager(models.Manager):
#     def get_exchanges_that_not_in_db(self):
#         exchanges = ManagerCCXT().exchanges
#         exchange_names = [exchange.id for exchange in exchanges]
#         db_exchanges_names = self.get_exchanges_names_in(exchange_names)
#         result_exchanges = set(exchange_names) - set(db_exchanges_names)
#         instances = [exchange for exchange in exchanges if exchange.id in result_exchanges]
#         return instances
#
#     def get_exchanges_names_in(self, exchange_names):
#         return self.filter(id_name__in=exchange_names).values_list('id_name', flat=True)


# class UnitManager(models.Manager):
#     def load_units(self, measurements=None):
#         if measurements:
#             self.filter(measurement__in=measurements)
#         units = self.values_list('pk', 'symbols', 'name', 'alias', named=True).distinct()
#
#         return list(units)
#
#     def get_missing_unit(self):
#         return self.get(name='Magnitud adimensional')

class MarketManager(models.Manager):
    def get_last_historical_date(self, market):
        last = self.get(pk=market.pk).ohlcv.last()

        if last:
            return last.date

        return self.model.FROM_DATE


class MarketOHLCVManager(models.Manager):
    def bulk_ohlcv(self, market: object, ohlcv: list) -> int:
        """To save a lot of data. It does not check whether the date for the market already exists.

        :param market: MarketOHLCV
        :param ohlcv: list

        by example:
        - MarketOHLCV('kraken', 'BTC/USD')
        - [[1550479200000, 3698.0, 3700.6, 3697.9, 3700.6, 5.0886]]
        """
        from itertools import islice
        batch_size = 250
        saved = 0

        objs = (self.model(market=market, date=parse_datetime(i[0]), open=i[1], hight=i[2], low=i[3], close=i[4],
                           volume=i[5]) for i in ohlcv)

        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                return saved
            self.bulk_create(batch, batch_size)
            saved = saved + len(batch)

    def add_price(self, market: object, ohlcv: list) -> int:
        """Update Or Create a price for x Martek of y Exchange.

        :param market: MarketOHLCV
        :param ohlcv: list
        """

        n_inserts = 0

        for i in ohlcv:
            obj, created = self.update_or_create(
                market=market,
                date=parse_datetime(i[0]),
                defaults={
                    'open': i[1],
                    'hight': i[2],
                    'low': i[3],
                    'close': i[4],
                    'volume': i[5]
                },
            )
            n_inserts = n_inserts if not created else n_inserts + 1

        return n_inserts
