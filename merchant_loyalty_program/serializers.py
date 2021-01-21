# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantLoyaltyProgram


class MerchantLoyaltyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantLoyaltyProgram
        fields = '__all__'


class MerchantLoyaltyProgramStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantLoyaltyProgram
        fields = [
            "id",
            "status"
        ]
