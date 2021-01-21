# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerCard


class CustomerCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCard
        fields = '__all__'


class CustomerCardStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCard
        fields = [
            "id",
            "status"
        ]


class CustomerCardCreateSerializer(serializers.Serializer):
    customer_id = serializers.CharField()
    card_number = serializers.CharField()
    card_exp_month = serializers.CharField()
    card_exp_year = serializers.CharField()
    card_cvc = serializers.CharField()
    card_name = serializers.CharField()
    card_email = serializers.CharField()
