import ccxt
import time
import logging

from django.core.management.base import BaseCommand

from src.exchanges.models import Market, MarketOHLCV

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "My shiny new management command."
    msec = 1000
    minute = 60 * msec

    def add_arguments(self, parser):
        parser.add_argument(
            'exchanges',
            help='All markets inside of exchange with id_name',
            nargs='+', type=str
        )
        parser.add_argument(
            '--markets',
            help='All markets with symbol',
            nargs='+', type=str
        )
        parser.add_argument(
            '--cycle',
            action='store_true',
            help='Keeps saving every "hold" seconds...'
        )
        parser.add_argument(
            '--hold',
            help='seconds for wait for next time.',
            type=int
        )
        parser.add_argument(
            '--toTs',
            help='timestamp for wait.',
            type=int
        )

    def handle(self, *args, **options):
        self.last_dates = {}
        hold = 60
        if options['hold']:
            hold = options['hold']
        filters = self._get_filters(options)
        markets = Market.objects.filter(**filters)

        while True:
            saved = 0
            for market in markets:
                try:
                    date = self.get_last_date(market)
                    self.stdout.write(f'Fetching candles in {market.exchange.name}-{market.symbol}, starting from: {date}')
                    ohlcv = market.fetch_ohlcv_history(from_timestamp=date)

                    if len(ohlcv) > 0:
                        first = ohlcv[0][0]
                        last = ohlcv[-1][0]
                        self.stdout.write(f'Fetching {len(ohlcv)}, from {first}, to {last}')
                        penultimate = ohlcv[-2][0]
                        saved = MarketOHLCV.objects.add_price(market=market, ohlcv=ohlcv[:-2])
                        self.last_dates[market.pk] = penultimate
                        self.stdout.write(f'last epoch candle in {market.symbol}, {penultimate}')
                except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) \
                        as error:

                    logger.error(type(error).__name__, error.args, ', retrying in', hold, 'seconds')

                finally:
                    self.stdout.write(self.style.SUCCESS(f'Saved {saved} in {market.symbol}...'))
                    time.sleep(hold)

            if not options['cycle'] or (options['toTs'] and date >= options['toTs']):
                return False

    def _get_filters(self, options):
        filters_map = {'exchanges': 'exchange__id_name__in', 'markets': 'symbol__in'}

        filters = {}
        for o in filters_map.keys():
            if o in options and options[o]:
                filters[filters_map.get(o)] = options[o]

        return filters

    def get_last_date(self, market):
        """ For return timestamp in this same format of milliseconds, it's necessary multiply by 1000 in the end

        :param market:
        :return:
        """
        if self.last_dates.get(market.pk):
            return self.last_dates.get(market.pk)

        return Market.objects.get_last_historical_date(market).timestamp() * self.msec
