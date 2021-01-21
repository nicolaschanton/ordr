# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerOrder
from merchant.serializers import PublicMerchantSerializer
from merchant_table.serializers import MerchantTableSerializer
from customer.serializers import PublicCustomerSerializer
from customer_order_line.serializers import MainCustomerOrderLineSerializer


class MainOrderSerializer(serializers.ModelSerializer):
    customer_order_lines = MainCustomerOrderLineSerializer(read_only=True, many=True)
    merchant = PublicMerchantSerializer(read_only=True, many=False)
    merchant_table = MerchantTableSerializer(read_only=True, many=False)
    customer = PublicCustomerSerializer(read_only=True, many=False)

    class Meta:
        model = CustomerOrder
        fields = [
            "id",
            "merchant",
            "merchant_table",
            "customer",
            "order_state",
            "order_paid_date",
            "order_started_preparation_date",
            "order_ended_preparation_date",
            "total_amount_vat_included",
            "total_amount_vat_excluded",
            "vat_amount_1",
            "vat_amount_2",
            "vat_amount_3",
            "created_date",
            "modified_date",
            "customer_order_lines",
        ]

