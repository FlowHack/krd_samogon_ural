# Generated by Django 4.0 on 2022-02-26 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_store', '0002_alter_order_options_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='characteristics',
        ),
    ]
