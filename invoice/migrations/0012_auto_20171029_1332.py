# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-29 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0011_invoice_is_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='sent_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]