# Generated by Django 2.2.5 on 2019-09-14 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_charge', '0003_merchantcharge_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantcharge',
            name='status',
            field=models.CharField(default='not captured', max_length=500),
        ),
    ]