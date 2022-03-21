# Generated by Django 4.0 on 2022-02-27 13:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_time_call_to_api'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time_call_to_api',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 13, 5, 53, 445096, tzinfo=utc), verbose_name='Последняя дата и время обращения к API'),
        ),
    ]