# Generated by Django 2.2.5 on 2020-04-19 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_order', '0001_initial'),
        ('merchant_invoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantinvoice',
            name='merchant_order',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='merchant_order.MerchantOrder'),
            preserve_default=False,
        ),
    ]