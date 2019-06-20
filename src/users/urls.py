from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic.base import RedirectView

from . import views
from src.orders.views import index


urlpatterns = [
    path('', RedirectView.as_view(url='/login')),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', index, name='home')
]
