# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-12 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0021_auto_20180512_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='paid_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
