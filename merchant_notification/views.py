# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters, mixins, generics
from django.db.models import Q
from datetime import datetime, timedelta

from .serializers import MerchantNotificationSerializer, ReadMerchantNotificationSerializer

from .models import MerchantNotification


class MerchantNotificationViewSet(viewsets.ModelViewSet):
    queryset = MerchantNotification.objects.all()

    def get_object(self):
        if self.action in ['retrieve', 'partial_update']:
            result = self.queryset.filter(merchant__user=self.request.user, id=self.kwargs["pk"]).first()
        else:
            result = self.queryset.filter(id=self.kwargs["pk"]).first()
        return result

    def get_queryset(self):
        if self.action in ['list_self']:
            queryset_target = self.queryset.filter(merchant__user=self.request.user)
        else:
            queryset_target = self.queryset
        return queryset_target

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'list_self']:
            serializer = MerchantNotificationSerializer
        elif self.action in ['partial_update']:
            serializer = ReadMerchantNotificationSerializer
        else:
            serializer = MerchantNotificationSerializer
        return serializer

    def get_permissions(self):
        if self.action in ['retrieve', 'partial_update', 'list_self']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def list_self(self, request):
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
