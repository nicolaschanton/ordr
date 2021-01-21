# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerOrderLine
from merchant_item.serializers import MainMerchantItemSerializer


class MainCustomerOrderLineSerializer(serializers.ModelSerializer):
    item = MainMerchantItemSerializer(read_only=True, many=False)

    class Meta:
        model = CustomerOrderLine
        fields = [
            "id",
            "order",
            "label",
            "quantity",
            "ready",
            "unit_amount_vat_included",
            "unit_amount_vat_excluded",
            "unit_vat_amount",
            "vat_rate",
            "total_amount_vat_included",
            "total_amount_vat_excluded",
            "total_vat_amount",
            "created_date",
            "modified_date",
            "item",
        ]

