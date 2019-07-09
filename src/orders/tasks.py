import logging
from celery import task

from django.core.mail import send_mail
from django.template.loader import get_template
from django.core.mail import EmailMessage

from src.orders.models import AlertTrade

logger = logging.getLogger(__name__)


@task
def raise_order(data):
    """
    Task to create order.
    :type data: dict {'market': <BTC/USD:string>, 'side': <buy|sell:string>, price': <float>}
    """
    AlertTrade.objects.create(symbol_market=data['market'], order_type=data['side'], price=data['price'])
    logger.info(f"raise_order({data})'")

    return data


@task
def send_notification(email, side, market, price, quantity):
    subject = "Crypstation"
    to = [email, ]
    from_email = "crypstation@gmail.com"
    logger.info(email, side, market, price, quantity)
    message = get_template("email/put_order.html").render({'email': email, 'side': side, 'market': market, 'price': price,
                                                      'quantity': quantity})
    email = EmailMessage(subject, message, bcc=to, from_email=from_email)
    email.content_subtype = "html"
    email.send()
