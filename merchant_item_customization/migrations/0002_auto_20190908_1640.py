# Generated by Django 2.2.5 on 2019-09-08 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_item_customization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantitemcustomization',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='merchant_item_customizations', to='merchant_item.MerchantItem'),
        ),
    ]
