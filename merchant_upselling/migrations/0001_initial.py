# Generated by Django 2.2.5 on 2020-04-23 21:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchant_item', '0004_auto_20190914_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantUpselling',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('item_1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='item_1', to='merchant_item.MerchantItem')),
                ('item_2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='item_2', to='merchant_item.MerchantItem')),
            ],
        ),
    ]