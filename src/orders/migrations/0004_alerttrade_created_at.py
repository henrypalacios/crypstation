# Generated by Django 2.2.2 on 2019-06-20 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20190618_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerttrade',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]