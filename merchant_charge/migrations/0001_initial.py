# Generated by Django 2.0.3 on 2019-09-06 19:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchant', '0001_initial'),
        ('merchant_bank_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantCharge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('charge_id', models.CharField(max_length=500)),
                ('captured', models.BooleanField(default=False)),
                ('amount', models.FloatField(default=0)),
                ('amount_refunded', models.FloatField(default=0)),
                ('currency', models.CharField(max_length=500)),
                ('created', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='merchant.Merchant')),
                ('merchant_bank_account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='merchant_bank_account.MerchantBankAccount')),
            ],
        ),
    ]
