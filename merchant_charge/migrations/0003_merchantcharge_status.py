# Generated by Django 2.2.5 on 2019-09-14 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_charge', '0002_remove_merchantcharge_merchant'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantcharge',
            name='status',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]