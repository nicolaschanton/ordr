# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters, mixins, generics
from django.db.models import Q
from datetime import datetime, timedelta
import sys

from .serializers import MerchantBankAccountSerializer, MerchantBankAccountUpdateSerializer

from .models import MerchantBankAccount
from merchant.models import Merchant
from utils.stripe_utils import create_merchant, update_merchant, create_bank_account, retrieve_merchant


class MerchantBankAccountViewSet(viewsets.ModelViewSet):
    queryset = MerchantBankAccount.objects.all()

    def get_object(self):
        if self.action in ['retrieve', 'partial_update', 'update', 'delete']:
            result = self.queryset.filter(id=self.kwargs["pk"]).first()

        elif self.action in ['retrieve_public', 'partial_update_public', 'update_public']:
            result = self.queryset.filter(id=self.kwargs["pk"]).first()

        elif self.action in ['retrieve_self', 'partial_update_self', 'update_self']:
            result = self.queryset.filter(merchant__user=self.request.user, id=self.kwargs["pk"]).first()
        else:
            result = self.queryset.filter(id=self.kwargs["pk"]).first()
        return result

    def get_queryset(self):
        if self.action in ['list']:
            result = self.queryset

        elif self.action in ['list_public']:
            result = self.queryset

        elif self.action in ['list_self']:
            result = self.queryset.filter(merchant__user=self.request.user, status='chargeable')

        else:
            result = self.queryset

        return result

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'partial_update', 'update', 'delete']:
            serializer = MerchantBankAccountSerializer

        elif self.action in ['list_public', 'retrieve_public', 'partial_update_public', 'update_public', 'delete_public']:
            serializer = MerchantBankAccountSerializer

        elif self.action in ['list_self', 'retrieve_self', 'update_self', 'delete_self']:
            serializer = MerchantBankAccountSerializer

        elif self.action in ['create']:
            serializer = MerchantBankAccountSerializer

        elif self.action in ['partial_update_self']:
            serializer = MerchantBankAccountUpdateSerializer

        else:
            serializer = MerchantBankAccountSerializer

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

    @action(detail=False, methods=['GET'])
    def list_self(self, request):
        try:
            page = self.paginate_queryset(self.get_queryset())
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
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
        try:
            data = request.data
            merchant = Merchant.objects.filter(id=data["merchant_id"]).first()

            if MerchantBankAccount.objects.filter(merchant=merchant).count() == 0:
                if merchant:
                    # Update thanks to Stripe Utils
                    if retrieve_merchant(merchant=merchant):

                        # Update Stripe Customer
                        update_merchant(
                            merchant=merchant,
                            email=merchant.email,
                            data={}
                        )

                    else:
                        # Create Stripe Customer
                        create_merchant(merchant=merchant)

                        # Update Stripe Customer
                        update_merchant(
                            merchant=merchant,
                            email=merchant.email,
                            data={}
                        )

                    try:
                        # Create Stripe Bank Account
                        res = create_bank_account(
                            merchant=merchant,
                            bank_iban=data["bank_account_iban"],
                            account_holder_name=data["bank_account_holder_name"],
                        )

                        return Response(status=status.HTTP_201_CREATED, data=MerchantBankAccountSerializer(res).data)

                    except:
                        print("ERROR: " + str(sys.exc_info()))
                        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "invalid bank account"})

                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "no matching customer"})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "existing bank account"})

        except:
            print("ERROR: " + str(sys.exc_info()))
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "something bad happened"})
