# Generated by Django 2.2.9 on 2020-01-25 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0015_auto_20190803_1846'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ['-pk'], 'verbose_name_plural': 'Vacancies'},
        ),
    ]