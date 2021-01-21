# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantItemSubCategory


class MerchantItemSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantItemSubCategory
        fields = '__all__'


class PublicMerchantItemSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantItemSubCategory
        fields = [
            "id",
            "merchant",
            "name",
            "status",
            "display_order",
            "url_tag",
            "created_date",
            "modified_date",
        ]


class MerchantItemSubCategoryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantItemSubCategory
        fields = [
            "id",
            "status",
        ]
