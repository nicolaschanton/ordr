# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer
from user.serializers import UserSerializer, PublicUserSerializer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class PublicCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'phone'
        ]


class CreateCustomerSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'

