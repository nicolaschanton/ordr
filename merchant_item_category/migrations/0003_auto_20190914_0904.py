# Generated by Django 2.2.5 on 2019-09-14 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_item_category', '0002_auto_20190908_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantitemcategory',
            name='url_tag',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
