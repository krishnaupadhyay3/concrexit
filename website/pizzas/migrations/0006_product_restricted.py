# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-13 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0005_auto_20171213_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='restricted',
            field=models.BooleanField(default=False),
        ),
    ]