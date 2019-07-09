import datetime
import factory
import factory.fuzzy
from factory.compat import UTC

from django.conf import settings
from django.contrib.auth.models import User

from . import models


class AlertTradeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AlertTrade
