# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 21:36
from __future__ import unicode_literals

from django.db import migrations, models


def remove_enddates(apps, schema_editor):
    Board = apps.get_model("activemembers", "Board")
    CommitteeMembership = apps.get_model("activemembers", "CommitteeMembership")
    for board in Board.objects.all():
        for membership in CommitteeMembership.objects.filter(committee=board):
            membership.until = None
            membership.save()


class Migration(migrations.Migration):

    dependencies = [
        ('activemembers', '0014_committee_active'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='board',
            managers=[
                ('objects', models.manager.Manager()),
            ],
        ),
        migrations.RunPython(remove_enddates),
    ]
