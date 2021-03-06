# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-12 08:31
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_event_send_cancel_email'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='registration',
            name='member_old',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='members.Member'),
        ),
    ]
