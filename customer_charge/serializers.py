# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerCharge


class CustomerChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCharge
        fields = '__all__'

