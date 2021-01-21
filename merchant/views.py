# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters, mixins, generics
from django.db.models import Q
from datetime import datetime, timedelta
import sys

from .serializers import MerchantSerializer, AuthenticatedMerchantSerializer, PublicMerchantSerializer, \
    MerchantUpdateSerializer
from merchant_item.serializers import MainMerchantItemSerializer

from .models import Merchant
from django.contrib.auth.models import User
from merchant_item.models import MerchantItem
from utils.stripe_utils import create_merchant


class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()

    def get_object(self):
        if self.action in ['retrieve', 'partial_update', 'update', 'delete']:
            result = self.queryset.filter(id=self.kwargs["pk"]).first()

        elif self.action in ['retrieve_public', 'partial_update_public', 'update_public']:
            result = self.queryset.filter(id=self.kwargs["pk"]).first()

        elif self.action in ['retrieve_self', 'partial_update_self', 'update_self']:
            result = self.queryset.filter(user=self.request.user, id=self.kwargs["pk"]).first()
        else:
            result = self.queryset.filter(id=self.kwargs["pk"]).first()
        return result

    def get_queryset(self):
        if self.action in ['list']:
            result = self.queryset

        elif self.action in ['list_public']:
            result = self.queryset

        elif self.action in ['list_self']:
            result = self.queryset.filter(user=self.request.user)

        else:
            result = self.queryset

        return result

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'partial_update', 'update', 'delete']:
            serializer = MerchantSerializer

        elif self.action in ['list_public', 'retrieve_public', 'partial_update_public', 'update_public', 'delete_public']:
            serializer = PublicMerchantSerializer

        elif self.action in ['list_self', 'retrieve_self', 'update_self', 'delete_self']:
            serializer = AuthenticatedMerchantSerializer

        elif self.action in ['create']:
            serializer = MerchantSerializer

        elif self.action in ['partial_update_self']:
            serializer = MerchantUpdateSerializer

        else:
            serializer = PublicMerchantSerializer

        return serializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'partial_update', 'update', 'delete']:
            permission_classes = [permissions.IsAdminUser]

        elif self.action in ['create', 'list_public', 'retrieve_public', 'partial_update_public', 'update_public', 'delete_public']:
            permission_classes = [permissions.AllowAny]

        elif self.action in ['list_self', 'retrieve_self', 'partial_update_self', 'update_self', 'delete_self']:
            permission_classes = [permissions.IsAuthenticated]

        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['GET'])
    def retrieve_self(self, request, pk):
        try:
            serializer = self.get_serializer(self.get_object(), many=False)
            if self.get_object():
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "bad request"})
        except:
            print("ERROR: " + str(sys.exc_info()))
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "bad request"})

    @action(detail=True, methods=['GET'])
    def retrieve_public(self, request, pk):
        try:
            serializer = self.get_serializer(self.get_object(), many=False)
            if self.get_object():
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "bad request"})
        except:
            print("ERROR: " + str(sys.exc_info()))
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "bad request"})

    @action(detail=True, methods=['PATCH'])
    def partial_update_self(self, request, pk=None):
        try:
            serializer = self.get_serializer(self.get_object(), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            print("ERROR: " + str(sys.exc_info()))
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "bad request"})

    def create(self, request, *args, **kwargs):
        data = request.data

        try:
            if User.objects.filter(username=data["user"]["username"]).count() == 0:

                # Split Owner Name
                name = data["owner_name"].split(" ")
                if len(name) >= 2:
                    first_name = data["owner_name"].split(" ")[0]
                    last_name = data["owner_name"].split(" ")[1]
                elif len(name) == 1:
                    first_name = data["owner_name"].split(" ")[0]
                    last_name = data["owner_name"]
                else:
                    first_name = ""
                    last_name = ""

                user = User.objects.create_user(
                    username=data["user"]["username"],
                    email=data["user"]["username"],
                    password=data["user"]["password"],
                    first_name=first_name,
                    last_name=last_name
                )
                merchant = Merchant(
                    user=user,
                    name=data["name"],
                    email=data["user"]["username"],
                    phone=data["phone"],
                    registration_number=data["registration_number"],
                    vat_number=data["vat_number"],
                    owner_name=data["owner_name"],
                    address_street=data["address_street"],
                    address_city=data["address_city"],
                    address_zip=data["address_zip"]
                )
                merchant.save()

                # Create Stripe Merchant
                create_merchant(merchant=merchant)

                return Response(status=status.HTTP_201_CREATED, data=AuthenticatedMerchantSerializer(merchant).data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "username already registered"})
        except:
            print("ERROR: " + str(sys.exc_info()))
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "something bad happened"})
