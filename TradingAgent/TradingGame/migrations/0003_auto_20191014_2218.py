# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-10-14 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TradingGame', '0002_auto_20191014_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='closing_price',
            field=models.FloatField(),
        ),
    ]
