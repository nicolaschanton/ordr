# Generated by Django 2.2.5 on 2020-04-26 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_item_customization_option', '0005_remove_merchantitemcustomizationoption_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantitemcustomizationoption',
            name='price_vat_excluded',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='merchantitemcustomizationoption',
            name='price_vat_included',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='merchantitemcustomizationoption',
            name='vat_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='merchantitemcustomizationoption',
            name='vat_rate',
            field=models.FloatField(default=0.2),
        ),
    ]
