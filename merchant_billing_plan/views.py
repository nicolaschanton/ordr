# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters, mixins, generics
from django.db.models import Q
from datetime import datetime, timedelta
import sys

from .serializers import MerchantBillingPlanSerializer

from .models import MerchantBillingPlan
from merchant.models import Merchant


class MerchantBillingPlanViewSet(viewsets.ModelViewSet):
    queryset = MerchantBillingPlan.objects.all()

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
            result = self.queryset.filter(merchant__user=self.request.user)

        else:
            result = self.queryset

        return result

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'partial_update', 'update', 'delete']:
            serializer = MerchantBillingPlanSerializer

        elif self.action in ['list_public', 'retrieve_public', 'partial_update_public', 'update_public', 'delete_public']:
            serializer = MerchantBillingPlanSerializer

        elif self.action in ['list_self', 'retrieve_self', 'partial_update_self', 'update_self', 'delete_self']:
            serializer = MerchantBillingPlanSerializer

        elif self.action in ['create']:
            serializer = MerchantBillingPlanSerializer

        else:
            serializer = MerchantBillingPlanSerializer

        return serializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve', 'partial_update', 'update', 'delete']:
            permission_classes = [permissions.IsAdminUser]

        elif self.action in ['list_public', 'retrieve_public', 'partial_update_public', 'update_public', 'delete_public']:
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
