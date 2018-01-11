# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-02 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0007_auto_20171213_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='restricted',
            field=models.BooleanField(default=False, help_text="Only allow to be ordered by people with the 'order restricted products' permission."),
        ),
    ]