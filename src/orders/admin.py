from django.contrib import admin

from src.exchanges.models import Account
from .models import AutomaticTrader, AlertTrade


@admin.register(AutomaticTrader)
class AutomaticTraderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_pair_amount', 'second_pair_amount', 'market_id')

    raw_id_fields = ('market_id',)


@admin.register(AlertTrade)
class AlertTradeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'symbol_market', 'order_side', 'price', 'strategy', 'created_at')

    list_filter = ('order_side', 'strategy', 'symbol_market')
    #search_fields = ('symbol_market')
    #raw_id_fields = ('author',)
    # prepopulated_fields = {'slug': ('title',)}
    # date_hierarchy = 'publish'
    # ordering = ('status', 'publish')
