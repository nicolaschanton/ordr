# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantOrder


class MerchantOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantOrder
        fields = '__all__'

