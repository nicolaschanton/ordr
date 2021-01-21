# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantBillingPlan


class MerchantBillingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantBillingPlan
        fields = '__all__'

