# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-10-09 10:21
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TradingGame', '0005_auto_20190928_0013'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdviseSetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_code', models.CharField(choices=[('0050', '元大台灣50(0050)'), ('2430', '燦坤(2430)')], max_length=4)),
                ('principal', models.IntegerField()),
                ('initialStockHold', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='setup',
            name='initial_transaction_date',
            field=models.DateField(choices=[(datetime.date(2016, 1, 4), '2016-01-04'), (datetime.date(2017, 1, 3), '2017-01-03')]),
        ),
        migrations.AlterField(
            model_name='setup',
            name='playing_duration',
            field=models.IntegerField(choices=[(60, '60個交易日(三個月)'), (240, '240個交易日(一年)')]),
        ),
        migrations.AlterField(
            model_name='setup',
            name='stock_code',
            field=models.CharField(choices=[('0050', '元大台灣50(0050)'), ('2430', '燦坤(2430)')], max_length=4),
        ),
        migrations.AlterField(
            model_name='setup',
            name='transaction_cost_rate',
            field=models.FloatField(choices=[(0.001425, '股票買賣現行手續費率(0.1425%)'), (0, '無')]),
        ),
    ]
