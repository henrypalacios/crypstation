import logging
from celery import task

from django.core.mail import send_mail

from src.exchanges.models import Market

logger = logging.getLogger(__name__)


@task
def raise_order(data):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    :type data: dict {'market': <Market.symbol:string>, 'price': <float>, }
    """
    #order = Order.objects.get(id=order_id)
    market = Market.objects.filter(exchange__account__isnull=False, symbol=data.get('market')).first()
    logger.info(f"order: {market.exchange}-{market.symbol}-{data.get('price')}'")

    return market