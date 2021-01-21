# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MerchantTable


class MerchantTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantTable
        fields = '__all__'

