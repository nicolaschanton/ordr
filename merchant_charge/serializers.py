# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantCharge
from merchant_bank_account.serializers import MerchantBankAccountSerializer


class MerchantChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantCharge
        fields = '__all__'

