from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'src.orders'
    verbose_name = "Orders"

    def ready(self):
        from . import signals
