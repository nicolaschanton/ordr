# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantItemCustomizationOption
from merchant_item.models import MerchantItem


class SimpleMerchantItemLevelOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantItem
        fields = '__all__'


class MainMerchantItemCustomizationOptionSerializer(serializers.ModelSerializer):
    item = SimpleMerchantItemLevelOneSerializer(many=False, read_only=True)

    class Meta:
        model = MerchantItemCustomizationOption
        fields = [
            "id",
            "item_customization",
            "default_quantity",
            "max_permitted",
            "min_permitted",
            "display_order",
            "price_vat_included",
            "price_vat_excluded",
            "vat_rate",
            "vat_amount",
            "created_date",
            "modified_date",
            "item",
        ]


class MerchantItemCustomizationOptionUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantItemCustomizationOption
        fields = [
            'id',
        ]

