# Generated by Django 2.2.5 on 2020-04-27 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_order_line', '0004_auto_20200419_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerorderline',
            name='item_customization',
        ),
        migrations.RemoveField(
            model_name='customerorderline',
            name='item_customization_option',
        ),
    ]