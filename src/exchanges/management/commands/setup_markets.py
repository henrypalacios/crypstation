from __future__ import print_function, unicode_literals
from PyInquirer import prompt
import ccxt

from django.core.management.base import BaseCommand

from src.exchanges.models import Exchange, Market


class Command(BaseCommand):
    help = "Initialized Markets command."

    def handle(self, *args, **options):
        exchanges = ccxt.exchanges

        questions = [
            {
                'type': 'list',
                'name': 'exchange',
                'message': 'Which exchange you want to add?',
                'choices': exchanges
            },
            {
                'type': 'checkbox',
                'name': 'markets',
                'message': 'Select Markets!',
                'choices': self._get_markets_options,
                'validate': lambda answer: 'You must choose at least one market.' \
                    if len(answer) == 0 else True
            },
        ]

        answers = prompt(questions)

        self._create_markets(answers)
        
    def _get_markets_options(self, answers):
        exchange_id = answers['exchange']
        exchange_class = getattr(ccxt, exchange_id)()

        options = exchange_class.load_markets()

        return [{'name': s} for s in exchange_class.symbols]

    def _create_markets(self, answers):
        exchange_id = answers.get('exchange')
        exchange = eval('ccxt.%s ()' % exchange_id)

        exchange_qs = Exchange.objects.filter(id_name=exchange_id).first()
        if not exchange_qs:
            exchange_qs = Exchange.objects.create(id_name=exchange_id, name=exchange.name)
            self.stdout.write(f'Saved Exchange {exchange_qs.name}')

        markets = answers.get('markets')
        db_markets = Market.objects.filter(symbol__in=markets, exchange=exchange_qs).values_list('symbol', flat=True)
        markets_not_db = set(markets) - set(db_markets)

        for m in markets_not_db:
            m = Market.objects.create(symbol=m, exchange=exchange_qs)
            self.stdout.write(self.style.SUCCESS(f'Saved {m.symbol} in {exchange_qs.name}'))