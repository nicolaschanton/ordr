# Generated by Django 2.2.5 on 2020-04-26 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_item', '0006_auto_20200426_0614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchantitem',
            name='is_displayed',
        ),
        migrations.AddField(
            model_name='merchantitem',
            name='is_option',
            field=models.BooleanField(default=False),
        ),
    ]