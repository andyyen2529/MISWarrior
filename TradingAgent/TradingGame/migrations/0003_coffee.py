# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-27 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TradingGame', '0002_auto_20190922_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coffee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
