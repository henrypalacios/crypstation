# Generated by Django 2.2.2 on 2019-06-07 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exchanges', '0003_auto_20190605_2346'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomaticTrader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_pair_amount', models.FloatField()),
                ('second_pair_amount', models.FloatField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allowed_trades', to='exchanges.Account')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='exchanges.Market')),
            ],
        ),
    ]
