# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantItem
from merchant_item_customization.serializers import MainMerchantItemCustomizationSerializer
from merchant_item_category.models import MerchantItemCategory


class MainMerchantItemSerializer(serializers.ModelSerializer):
    merchant_item_customizations = MainMerchantItemCustomizationSerializer(many=True, read_only=True)

    class Meta:
        model = MerchantItem
        fields = [
            "id",
            "merchant",
            "category",
            "name",
            "description",
            "price_vat_included",
            "price_vat_excluded",
            "vat_rate",
            "vat_amount",
            "article_image",
            "status",
            "display_order",
            "has_happy_hour",
            "happy_hour_start_hour",
            "happy_hour_end_hour",
            "url_tag",
            "created_date",
            "modified_date",
            "merchant_item_customizations",
        ]


class MerchantItemStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantItem
        fields = [
            "id",
            "status",
        ]


class MerchantItemCategoryWithItemsStatusSerializer(serializers.ModelSerializer):
    merchant_items = MainMerchantItemSerializer(many=True, read_only=True)

    class Meta:
        model = MerchantItemCategory
        fields = [
            "id",
            "name",
            "display_order",
            "status",
            "merchant_items"
        ]
