# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 20:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('since', models.DateField(default=django.utils.timezone.now, help_text='Hide this announcement before this time.', verbose_name='Display since')),
                ('until', models.DateField(blank=True, help_text='Hide this announcement after this time.', null=True, verbose_name='Display until')),
                ('icon', models.CharField(default='bullhorn', help_text='Font Awesome abbreviation for icon to use.', max_length=150, verbose_name='Font Awesome icon')),
                ('closeable', models.BooleanField(default=True)),
                ('content_en', models.CharField(help_text='The content of the announcement; what text to display.', max_length=500, verbose_name='Content (EN)')),
                ('content_nl', models.CharField(help_text='The content of the announcement; what text to display.', max_length=500, verbose_name='Content (NL)')),
            ],
            options={
                'ordering': ('-since',),
            },
        ),
    ]
