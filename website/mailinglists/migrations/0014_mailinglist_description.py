# Generated by Django 2.2.1 on 2019-09-25 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailinglists', '0013_auto_20180901_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailinglist',
            name='description',
            field=models.TextField(default='Description default', help_text='Write a description for the mailinglist.', verbose_name='Description'),
            preserve_default=False,
        ),
    ]
