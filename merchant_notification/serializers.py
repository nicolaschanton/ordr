# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantNotification


class MerchantNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantNotification
        fields = '__all__'


class ReadMerchantNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantNotification
        fields = [
            "merchant",
            "read"
        ]
