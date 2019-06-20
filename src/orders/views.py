from django.shortcuts import render
from django.core.paginator import Paginator

from src.orders.models import AlertTrade


def index(request):
    alerts = AlertTrade.objects.order_by('-created_at')

    paginator = Paginator(alerts, 15)
    page = request.GET.get('page')
    paged = paginator.get_page(page)

    context = {
        'alerts': paged
    }

    return render(request, 'orders/alerttrades_list.html', context)
