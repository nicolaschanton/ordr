# Generated by Django 2.0.3 on 2019-09-06 19:13

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer_order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerInvoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invoice_file', models.FileField(blank=True, null=True, upload_to='customer_invoices/')),
                ('invoice_number', models.IntegerField(default=1)),
                ('invoice_number_text', models.CharField(max_length=100)),
                ('invoice_date', models.DateField(default=datetime.date.today)),
                ('invoice_street', models.CharField(max_length=500)),
                ('invoice_city', models.CharField(max_length=500)),
                ('invoice_zip', models.CharField(max_length=500)),
                ('invoice_company_name', models.CharField(max_length=500)),
                ('invoice_customer_name', models.CharField(max_length=500)),
                ('invoice_paid', models.BooleanField(default=True)),
                ('invoice_vat_amount_1', models.FloatField(default=0)),
                ('invoice_vat_amount_2', models.FloatField(default=0)),
                ('invoice_vat_amount_3', models.FloatField(default=0)),
                ('invoice_total_amount_vat_included', models.FloatField(default=0)),
                ('invoice_total_amount_vat_excluded', models.FloatField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer_order.CustomerOrder')),
            ],
        ),
    ]
