import ast
from os.path import join as join_path

from django.conf import settings

exchanges = ['bitfinex2', 'coinmarketcap', 'kraken', 'poloniex']


class Exchange:
    path = join_path(settings.BASE_DIR, '../src/exchanges/extras/markets.txt')

    def __init__(self):
        self._read_markets()

    def load_markets(self):
        return self.markets

    def _read_markets(self):
        with open(self.path, 'r') as f:
            s = f.read()
            self.markets = ast.literal_eval(s)


class bitfinex2(Exchange):
    def __init__(self):
        super().__init__()
        self.id = 'bitfinex2'
        self.name = 'Bitfinex V2'


class coinmarketcap(Exchange):
    def __init__(self):
        super().__init__()
        self.id = 'coinmarketcap'
        self.name = 'CoinMarketCap'


class kraken(Exchange):
    def __init__(self):
        super().__init__()
        self.id = 'kraken'
        self.name = 'Kraken'


class poloniex(Exchange):
    def __init__(self):
        super().__init__()
        self.id = 'poloniex'
        self.name = 'Poloniex'
