# Generated by Django 2.2.5 on 2019-09-14 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_bank_account', '0003_auto_20190914_1007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchantbankaccount',
            name='account_holder_type',
        ),
        migrations.RemoveField(
            model_name='merchantbankaccount',
            name='bank_name',
        ),
        migrations.RemoveField(
            model_name='merchantbankaccount',
            name='country',
        ),
        migrations.RemoveField(
            model_name='merchantbankaccount',
            name='fingerprint',
        ),
        migrations.RemoveField(
            model_name='merchantbankaccount',
            name='last4',
        ),
        migrations.RemoveField(
            model_name='merchantbankaccount',
            name='metadata',
        ),
        migrations.RemoveField(
            model_name='merchantbankaccount',
            name='routing_number',
        ),
        migrations.RemoveField(
            model_name='merchantbankaccount',
            name='stripe_customer_id',
        ),
        migrations.AddField(
            model_name='merchantbankaccount',
            name='client_secret',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='merchantbankaccount',
            name='sd_bank_code',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='merchantbankaccount',
            name='sd_country',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='merchantbankaccount',
            name='sd_fingerprint',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='merchantbankaccount',
            name='sd_last4',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='merchantbankaccount',
            name='sd_mandate_reference',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='merchantbankaccount',
            name='sd_mandate_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='merchantbankaccount',
            name='type',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='merchantbankaccount',
            name='usage',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='merchantbankaccount',
            name='currency',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='merchantbankaccount',
            name='status',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='merchantbankaccount',
            name='stripe_bank_account_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]