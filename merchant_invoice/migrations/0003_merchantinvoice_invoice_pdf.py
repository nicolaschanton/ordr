# Generated by Django 2.2.5 on 2020-04-19 22:20

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_invoice', '0002_merchantinvoice_merchant_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantinvoice',
            name='invoice_pdf',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='file'),
        ),
    ]