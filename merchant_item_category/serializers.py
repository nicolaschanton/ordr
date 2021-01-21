# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantItemCategory
from merchant_item_sub_category.serializers import MerchantItemSubCategorySerializer


class PublicMerchantItemCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantItemCategory
        fields = [
            "id",
            "name",
            "merchant",
            "status",
            "display_order",
            "url_tag",
        ]


class MerchantItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantItemCategory
        fields = '__all__'


class MerchantItemCategoryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantItemCategory
        fields = [
            "id",
            "status",
        ]
