# Generated by Django 2.0.3 on 2019-09-06 19:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantBillingPlan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('starting_date', models.DateField(default=django.utils.timezone.now)),
                ('base_monthly_fees_vat_excluded', models.FloatField(default=0)),
                ('base_monthly_fees_vat_included', models.FloatField(default=0)),
                ('base_monthly_fees_vat_amount', models.FloatField(default=0)),
                ('variable_fees_vat_excluded', models.FloatField(default=0)),
                ('variable_fees_vat_included', models.FloatField(default=0)),
                ('variable_fees_vat_amount', models.FloatField(default=0)),
                ('is_indexed_on_order_number', models.BooleanField(default=False)),
                ('is_indexed_on_order_amount', models.BooleanField(default=False)),
                ('fees_per_order_vat_excluded', models.FloatField(default=0)),
                ('fees_per_order_vat_included', models.FloatField(default=0)),
                ('fees_per_order_vat_amount', models.FloatField(default=0)),
                ('fees_per_euro_vat_excluded', models.FloatField(default=0)),
                ('fees_per_euro_vat_included', models.FloatField(default=0)),
                ('fees_per_euro_vat_amount', models.FloatField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('merchant', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='merchant.Merchant')),
            ],
        ),
    ]
