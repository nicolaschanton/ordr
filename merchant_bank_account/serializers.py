# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantBankAccount


class MerchantBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantBankAccount
        fields = '__all__'


class MerchantBankAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantBankAccount
        fields = [
            "id",
            "merchant",
            "status"
        ]
