# Generated by Django 3.1.1 on 2020-09-07 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0011_album_new_album_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='title_nl',
        ),
    ]
