# Generated by Django 2.2.5 on 2019-09-08 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_item_customization', '0002_auto_20190908_1640'),
        ('merchant_item_customization_option', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchantitemcustomizationoption',
            name='item',
        ),
        migrations.AddField(
            model_name='merchantitemcustomizationoption',
            name='item_customization',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='merchant_item_customization_options', to='merchant_item_customization.MerchantItemCustomization'),
            preserve_default=False,
        ),
    ]