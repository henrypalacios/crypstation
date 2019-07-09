import logging

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import AlertTrade, AutomaticTrader

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AlertTrade)
def fire_execute_order(sender, instance, **kwargs):
    logger.debug("Fire AutomatedTrader for market %s", instance.symbol_market)
    AutomaticTrader.objects.execute_order(instance)
