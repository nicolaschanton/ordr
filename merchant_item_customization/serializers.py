# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantItemCustomization
from merchant_item_customization_option.serializers import MainMerchantItemCustomizationOptionSerializer


class MainMerchantItemCustomizationSerializer(serializers.ModelSerializer):
    merchant_item_customization_options = MainMerchantItemCustomizationOptionSerializer(many=True, read_only=True)

    class Meta:
        model = MerchantItemCustomization
        fields = [
            "id",
            "item",
            "name",
            "max_permitted",
            "min_permitted",
            "status",
            "display_order",
            "created_date",
            "modified_date",
            "merchant_item_customization_options"
        ]


class MerchantItemCustomizationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantItemCustomization
        fields = [
            "id",
            "status",
        ]
