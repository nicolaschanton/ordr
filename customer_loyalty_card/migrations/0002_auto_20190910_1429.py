# Generated by Django 2.2.5 on 2019-09-10 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_loyalty_program', '0003_merchantloyaltyprogram_status'),
        ('customer', '0001_initial'),
        ('customer_loyalty_card', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerLoyaltyCardDetails',
            new_name='CustomerLoyaltyCardHistory',
        ),
    ]
