# Generated by Django 2.2.5 on 2019-09-10 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_loyalty_program', '0002_merchantloyaltyprogram_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantloyaltyprogram',
            name='status',
            field=models.CharField(choices=[('act', 'Active'), ('tbr', 'To be reviewed by admin'), ('unv', 'Unavailable'), ('dlt', 'Deleted')], default='tbr', max_length=3),
        ),
    ]