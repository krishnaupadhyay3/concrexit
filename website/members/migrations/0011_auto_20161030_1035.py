# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_merge_20160907_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='show_birthday',
            field=models.BooleanField(default=True, help_text='Show your birthday to other members on your profile page and in the birthday calendar', verbose_name='Display birthday'),
        ),
    ]
