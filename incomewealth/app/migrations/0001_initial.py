# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 23:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeWealth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
                ('income_top10', models.FloatField()),
                ('wealth_top10', models.FloatField()),
                ('income_bottom50', models.FloatField()),
                ('wealth_bottom50', models.FloatField()),
            ],
        ),
    ]
