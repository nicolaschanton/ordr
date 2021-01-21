# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerNotification


class CustomerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerNotification
        fields = '__all__'


class CustomerNotificationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerNotification
        fields = [
            "id",
            "read"
        ]

