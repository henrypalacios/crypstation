from django.contrib import admin
from django.forms import ModelForm, PasswordInput

from .models import Account


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['apiKey', 'secret', 'password', 'uid', 'exchange']
        widgets = {
            'apiKey': PasswordInput(),
            'secret': PasswordInput(),
            'password': PasswordInput(),
        }


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    form = AccountForm
    list_display = ('pk', 'uid', 'exchange')
