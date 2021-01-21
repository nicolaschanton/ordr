# Generated by Django 2.2.5 on 2020-04-22 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0005_auto_20200422_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='address_city',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='address_street',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='address_zip',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='owner_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='registration_number',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='vat_number',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]