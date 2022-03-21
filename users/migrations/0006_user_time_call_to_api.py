# Generated by Django 4.0 on 2022-02-27 12:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_emailsformessages'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='time_call_to_api',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Последняя дата и время обращения к API'),
        ),
    ]
