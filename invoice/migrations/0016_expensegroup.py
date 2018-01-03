# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-03 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0015_auto_20180102_0048'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('expense', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='invoice.Invoice')),
            ],
        ),
    ]