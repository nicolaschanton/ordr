# Generated by Django 2.2.5 on 2019-09-07 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_billing_plan', '0003_auto_20190907_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantbillingplan',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='merchant.Merchant'),
        ),
    ]