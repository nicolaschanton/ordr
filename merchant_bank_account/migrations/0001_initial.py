# Generated by Django 2.0.3 on 2019-09-06 19:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantBankAccount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bank_iban', models.CharField(blank=True, max_length=500, null=True)),
                ('account_holder_name', models.CharField(blank=True, max_length=500, null=True)),
                ('stripe_bank_account_id', models.CharField(blank=True, max_length=100, null=True)),
                ('account_holder_type', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('currency', models.CharField(blank=True, max_length=100, null=True)),
                ('stripe_customer_id', models.CharField(blank=True, max_length=100, null=True)),
                ('fingerprint', models.CharField(blank=True, max_length=100, null=True)),
                ('last4', models.CharField(blank=True, max_length=100, null=True)),
                ('metadata', models.CharField(blank=True, max_length=100, null=True)),
                ('routing_number', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('merchant', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='merchant.Merchant')),
            ],
        ),
    ]
