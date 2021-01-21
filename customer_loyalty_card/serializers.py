# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerLoyaltyCard, CustomerLoyaltyCardHistory


class CustomerLoyaltyCardHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLoyaltyCardHistory
        fields = '__all__'


class CustomerLoyaltyCardSerializer(serializers.ModelSerializer):
    customer_loyalty_card_histories = CustomerLoyaltyCardHistorySerializer(read_only=True, many=True)

    class Meta:
        model = CustomerLoyaltyCard
        fields = [
            "id",
            "loyalty_program",
            "customer",
            "point_count",
            "deleted",
            "created_date",
            "modified_date",
            "customer_loyalty_card_histories"
        ]

