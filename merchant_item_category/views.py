# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters, mixins, generics
from django.db.models import Q
from datetime import datetime, timedelta
import sys

from .serializers import MerchantItemCategorySerializer, MerchantItemCategoryStatusSerializer

from merchant_item.serializers import MerchantItemCategoryWithItemsStatusSerializer

from .models import MerchantItemCategory
from merchant_table.models import MerchantTable


class MerchantItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = MerchantItemCategory.objects.all()

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
            try:
                merchant = MerchantTable.objects.get(id=self.request.query_params["merchant_table_id"]).merchant
                result = self.queryset.filter(merchant=merchant, status="ac")
            except:
                result = None

        elif self.action in ['list_public_with_items']:
            try:
                merchant = MerchantTable.objects.get(id=self.request.query_params["merchant_table_id"]).merchant
                result = self.queryset.filter(merchant=merchant, status="ac")
            except:
                result = None

        elif self.action in ['list_self']:
            result = self.queryset.filter(merchant__user=self.request.user)

        else:
            result = self.queryset

        return result

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'partial_update', 'update', 'delete']:
            serializer = MerchantItemCategorySerializer

        elif self.action in ['list_public', 'retrieve_public', 'partial_update_public', 'update_public',
                             'delete_public']:
            serializer = MerchantItemCategorySerializer

        elif self.action in ['list_self', 'retrieve_self', 'update_self', 'delete_self']:
            serializer = MerchantItemCategorySerializer

        elif self.action in ['create']:
            serializer = MerchantItemCategorySerializer

        elif self.action in ['partial_update_self']:
            serializer = MerchantItemCategoryStatusSerializer

        elif self.action in ['list_public_with_items']:
            serializer = MerchantItemCategoryWithItemsStatusSerializer

        else:
            serializer = MerchantItemCategorySerializer

        return serializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve', 'partial_update', 'update', 'delete']:
            permission_classes = [permissions.IsAdminUser]

        elif self.action in ['list_public_with_items', 'list_public', 'retrieve_public', 'partial_update_public', 'update_public',
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

    @action(detail=False, methods=['GET'])
    def list_public(self, request):
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

    @action(detail=False, methods=['GET'])
    def list_public_with_items(self, request):
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
