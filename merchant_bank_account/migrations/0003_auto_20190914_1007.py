# Generated by Django 2.2.5 on 2019-09-14 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_bank_account', '0002_auto_20190907_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantbankaccount',
            name='merchant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='merchant.Merchant'),
        ),
    ]