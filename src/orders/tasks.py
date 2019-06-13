import logging
from celery import task

from django.core.mail import send_mail

from src.exchanges.models import Market
from src.orders.models import AutomaticTrader, AlertTrade

logger = logging.getLogger(__name__)


@task
def raise_order(data):
    """
    Task to create order.
    :type data: dict {'market': <BTC/USD:string>, 'side': <buy|sell:string>, price': <float>}
    """
    AlertTrade.objects.create(symbol_market=data['market'], order_type=data['side'], price=data['price'])
    logger.info(f"order: {data}'")

    return data
