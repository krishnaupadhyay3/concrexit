# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-08 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('pizzas', '0006_product_restricted'), ('pizzas', '0007_auto_20171213_2017'), ('pizzas', '0008_auto_20180102_1635')]

    dependencies = [
        ('pizzas', '0005_auto_20171213_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='restricted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',), 'permissions': (('order_restricted_products', 'Order restricted products'),)},
        ),
        migrations.AlterModelManagers(
            name='product',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='restricted',
            field=models.BooleanField(default=False, help_text="Only allow to be ordered by people with the 'order restricted products' permission."),
        ),
    ]
