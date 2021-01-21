# Generated by Django 2.0.3 on 2019-09-06 19:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer_credit_card', '0001_initial'),
        ('merchant', '0001_initial'),
        ('merchant_table', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_state', models.CharField(choices=[('dr', 'Draft'), ('pa', 'Paid'), ('pr', 'In Preparation'), ('do', 'Done'), ('er', 'Payment Error'), ('re', 'Refused'), ('rf', 'Refunded'), ('de', 'Deleted')], default='dr', max_length=2)),
                ('order_paid_date', models.DateTimeField(blank=True, null=True)),
                ('order_started_preparation_date', models.DateTimeField(blank=True, null=True)),
                ('order_ended_preparation_date', models.DateTimeField(blank=True, null=True)),
                ('total_amount_vat_included', models.FloatField(default=0)),
                ('total_amount_vat_excluded', models.FloatField(default=0)),
                ('vat_amount_1', models.FloatField(default=0)),
                ('vat_amount_2', models.FloatField(default=0)),
                ('vat_amount_3', models.FloatField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer.Customer')),
                ('customer_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='customer_credit_card.CustomerCard')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='merchant.Merchant')),
                ('merchant_table', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='merchant_table.MerchantTable')),
            ],
        ),
    ]