import time

# from src.exchanges.models import Exchange, Market

msec = 1000
minute = 60 * msec
hold = 30


def get_api_ccxt():
    from src.exchanges import api_ccxt
    return api_ccxt


class ManagerCCXT:

    def __init__(self):
        self.ccxt = get_api_ccxt()
        self.exchanges = self.get_instances()

    # @classmethod
    # def get_exchange(cls, exchange_name):
    #     return cls(exchange_name).exchange
    #
    # def get_historical_data(self, market, from_date, timeframe='1h'):
    #     try:
    #         from_timestamp = self.exchange.parse8601(from_date)
    #         ohlcvs = self.exchange.fetch_ohlcv(market, timeframe, from_timestamp)
    #     except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
    #         return error
    #
    #     return ohlcvs

    def get_instances(self):
        return [getattr(self.ccxt, e)() for e in self.ccxt.exchanges]

# class ManagerExchanges:
#
#     def __init__(self):
#         self.exchanges = self.get_exchanges()
#
#     @staticmethod
#     def get_exchanges():
#         return [getattr(ccxt, e)() for e in ccxt.exchanges]
#
#     @classmethod
#     def get_exchanges_that_not_in_db(cls):
#         manager = cls()
#         exchange_names = [exchange.id for exchange in manager.exchanges]
#         db_exchanges = Exchange.objects.filter(id_name__in=exchange_names).values_list('id_name', flat=True)
#         result_exchanges = set(exchange_names) - set(db_exchanges)
#         instances = [exchange for exchange in manager.exchanges if exchange.id in result_exchanges]
#         return instances
#
#     @classmethod
#     def get_markets_that_not_in_db(cls, name_exchange):
#         manager = cls()
#         if name_exchange in [e.id for e in manager.exchanges]:
#             instance = [e for e in manager.exchanges if e.id in name_exchange][0]
#             markets_names = [name for name in instance.load_markets()]
#             db_markets = Market.objects\
#                 .filter(id_name__in=markets_names)\
#                 .values_list('id_name', flat=True)
#             result_markets = set(markets_names) - set(db_markets)
#             markets = instance.load_markets()
#             return {k: v for k, v in markets.items() if k in result_markets}

# class MarketService:
#     @staticmethod
#     def set_historical_price(exchange, market_name, from_date):
#         exchange = ExchangeAPI(exchange)
#         data = exchange.get_historical_data(market_name, from_date)
#
#         MarketOHLCV.objects.bulk_ohlcv(data)
