# Generated by Django 2.2.5 on 2019-09-08 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0002_auto_20190907_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='merchants', to=settings.AUTH_USER_MODEL),
        ),
    ]
