import logging
from celery import task

from django.core.mail import send_mail

from src.exchanges.models import Market
from src.orders.models import AllowedTrade

logger = logging.getLogger(__name__)


@task
def raise_order(data):
    """
    Task to create order.
    :type data: dict {'market': <Market.symbol:string>, 'side': <buy|sell:string>, price': <float>}
    """
    AllowedTrade.objects.fire_order(data['market'], data['side'], data['price'])
    logger.info(f"order: {data}'")

    return data