# Generated by Django 2.2.5 on 2020-04-26 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_item', '0005_merchantitem_is_displayed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantitem',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='merchant_items', to='merchant_item_sub_category.MerchantItemSubCategory'),
        ),
    ]
