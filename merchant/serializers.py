# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Merchant
from user.serializers import UserSerializer, PublicUserSerializer
from merchant_item.models import MerchantItem
from merchant_item.serializers import MainMerchantItemSerializer
from merchant_item_category.serializers import PublicMerchantItemCategorySerializer


class MerchantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Merchant
        fields = '__all__'


class MerchantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "open",
            "registration_number",
            "vat_number",
            "owner_name",
            "address_street",
            "address_city",
            "address_zip",
            "accept_cash",
            "accept_service_bar",
            "accept_service_table",
            "shop_description",
        ]


class AuthenticatedMerchantSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = Merchant
        fields = '__all__'


class PublicMerchantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Merchant
        fields = [
            "id",
            "name",
            "presentation_image",
            "open",
            "address_street",
            "address_city",
            "address_zip",
            "shop_description",
            "accept_cash",
            "accept_service_bar",
            "accept_service_table",
        ]
