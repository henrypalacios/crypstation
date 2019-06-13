import logging

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import AlertTrade

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AlertTrade)
def fire_execute_order(sender, instance, **kwargs):
    logger.error("Fire AutomatedTrader for market %s", instance.symbol_market)
