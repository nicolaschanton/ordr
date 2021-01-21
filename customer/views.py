# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters, mixins, generics
from django.db.models import Q
from datetime import datetime, timedelta
import sys

from .serializers import CustomerSerializer, CreateCustomerSerializer

from .models import Customer
from django.contrib.auth.models import User
from utils.stripe_utils import create_customer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()

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
            serializer = CustomerSerializer

        elif self.action in ['list_public', 'retrieve_public', 'partial_update_public', 'update_public', 'delete_public']:
            serializer = CustomerSerializer

        elif self.action in ['list_self', 'retrieve_self', 'partial_update_self', 'update_self', 'delete_self']:
            serializer = CustomerSerializer

        elif self.action in ['create']:
            serializer = CreateCustomerSerializer

        else:
            serializer = CustomerSerializer

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

            user_search = User.objects.filter(username=data["user"]["username"])

            if user_search.count() == 0:
                user = User.objects.create_user(
                    username=data["user"]["username"],
                    email=data["user"]["username"],
                    password=data["user"]["password"],
                    first_name=data["first_name"],
                    last_name=data["last_name"]
                )
                customer = Customer(
                    user=user,
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    phone=data["phone"],
                    email=data["user"]["username"]
                )
                customer.save()

                # Create Stripe Customer
                create_customer(customer=customer)

                return Response(status=status.HTTP_201_CREATED, data=CustomerSerializer(customer).data)

            elif user_search.count() == 1:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "username already registered"})
        except:
            print("ERROR: " + str(sys.exc_info()))
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "something bad happened"})

