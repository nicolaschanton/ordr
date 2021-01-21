# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantInvoice


class MerchantInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantInvoice
        fields = '__all__'

