# Generated by Django 2.2.5 on 2019-09-13 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_loyalty_program', '0003_merchantloyaltyprogram_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchantloyaltyprogram',
            name='active',
        ),
    ]