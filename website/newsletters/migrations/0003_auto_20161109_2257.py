# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-09 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0002_auto_20161109_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletterevent',
            name='penalty_costs',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, help_text='This is the price that a member has to pay when he/she did not show up.', max_digits=5, null=True, verbose_name='Costs (in Euro)'),
        ),
    ]
