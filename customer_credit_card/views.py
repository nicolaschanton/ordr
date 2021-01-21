# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters, mixins, generics
from django.db.models import Q
from datetime import datetime, timedelta
import sys

from .serializers import CustomerCardSerializer, CustomerCardStatusSerializer, CustomerCardCreateSerializer

from .models import CustomerCard
from customer.models import Customer
from utils.stripe_utils import create_customer, create_credit_card, update_customer, \
    retrieve_customer


class CustomerCardViewSet(viewsets.ModelViewSet):
    queryset = CustomerCard.objects.all()

    def get_object(self):
        if self.action in ['retrieve', 'partial_update', 'update', 'delete']:
            result = self.queryset.filter(id=self.kwargs["pk"]).first()

        elif self.action in ['retrieve_public', 'partial_update_public', 'update_public']:
            result = self.queryset.filter(id=self.kwargs["pk"]).first()

        elif self.action in ['retrieve_self', 'partial_update_self', 'update_self']:
            result = self.queryset.filter(customer__user=self.request.user, id=self.kwargs["pk"]).first()
        else:
            result = self.queryset.filter(id=self.kwargs["pk"]).first()
        return result

    def get_queryset(self):
        if self.action in ['list']:
            result = self.queryset

        elif self.action in ['list_public']:
            result = self.queryset

        elif self.action in ['list_self']:
            result = self.queryset.filter(customer__user=self.request.user)

        else:
            result = self.queryset

        return result

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'partial_update', 'update', 'delete']:
            serializer = CustomerCardSerializer

        elif self.action in ['list_public', 'retrieve_public', 'partial_update_public', 'update_public',
                             'delete_public']:
            serializer = CustomerCardSerializer

        elif self.action in ['list_self', 'retrieve_self', 'update_self', 'delete_self']:
            serializer = CustomerCardSerializer

        elif self.action in ['create']:
            serializer = CustomerCardCreateSerializer

        elif self.action in ['partial_update_self']:
            serializer = CustomerCardStatusSerializer

        else:
            serializer = CustomerCardSerializer

        return serializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'partial_update', 'update', 'delete']:
            permission_classes = [permissions.IsAdminUser]

        elif self.action in ['create', 'list_public', 'retrieve_public', 'partial_update_public', 'update_public',
                             'delete_public']:
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
            customer = Customer.objects.filter(id=data["customer_id"]).first()

            if customer:
                # Update thanks to Stripe Utils
                if retrieve_customer(customer=customer):

                    # Update Stripe Customer
                    update_customer(
                        customer=customer,
                        email=data["card_email"] if not customer.email else customer.email,
                        data={}
                    )

                else:
                    # Create Stripe Customer
                    create_customer(customer=customer)

                    # Update Stripe Customer
                    update_customer(
                        customer=customer,
                        email=data["card_email"] if not customer.email else customer.email,
                        data={}
                    )

                try:
                    # Create Stripe Card
                    res = create_credit_card(
                        customer=customer,
                        number=data["card_number"],
                        exp_month=data["card_exp_month"],
                        exp_year=data["card_exp_year"],
                        cvc=data["card_cvc"],
                        name=data["card_name"],
                        email=data["card_email"],
                    )

                    return Response(status=status.HTTP_201_CREATED, data=CustomerCardSerializer(res).data)

                except:
                    print("ERROR: " + str(sys.exc_info()))
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "invalid credit card"})

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "no matching customer"})

        except:
            print("ERROR: " + str(sys.exc_info()))
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "something bad happened"})
