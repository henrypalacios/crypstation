# Generated by Django 2.2.2 on 2019-06-18 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alerttrade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alerttrade',
            name='order_type',
            field=models.CharField(choices=[('buy', 'BUY'), ('sell', 'SELL')], max_length=5),
        ),
    ]
