# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantUpselling


class MerchantUpsellingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantUpselling
        fields = '__all__'

