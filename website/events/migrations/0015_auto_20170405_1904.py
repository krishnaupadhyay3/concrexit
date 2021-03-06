# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 17:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20170403_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organiser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='activemembers.Committee', verbose_name='organiser'),
            preserve_default=False,
        ),
    ]
