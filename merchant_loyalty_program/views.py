# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters, mixins, generics
from django.db.models import Q
from datetime import datetime, timedelta

from .serializers import MerchantLoyaltyProgramSerializer, MerchantLoyaltyProgramStatusSerializer

from .models import MerchantLoyaltyProgram


class MerchantLoyaltyProgramViewSet(viewsets.ModelViewSet):
    queryset = MerchantLoyaltyProgram.objects.all()

    def get_object(self):
        if self.action in ['retrieve', 'partial_update']:
            result = self.queryset.filter(id=self.kwargs["pk"]).first()
        elif self.action in ['partial_update_status']:
            result = self.queryset.filter(id=self.kwargs["pk"], merchant__user=self.request.user).first()
        else:
            result = ""
        return result

    def get_queryset(self):
        if self.action in ['list_self']:
            queryset_target = self.queryset.filter(merchant__user=self.request.user)
        else:
            queryset_target = self.queryset
        return queryset_target

    def get_serializer_class(self):
        if self.action in ['retrieve', 'partial_update', 'create', 'list_self']:
            serializer = MerchantLoyaltyProgramSerializer
        elif self.action in ['partial_update_status']:
            serializer = MerchantLoyaltyProgramSerializer
        else:
            serializer = MerchantLoyaltyProgramSerializer
        return serializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list_self', 'partial_update_status']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def partial_update_status(self, request, pk=None):
        merchant_loyalty_program = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            merchant_loyalty_program.status = serializer.data['status']
            merchant_loyalty_program.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data=MerchantLoyaltyProgramStatusSerializer(merchant_loyalty_program).data
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'something bad happened'})

    @action(detail=False)
    def list_self(self, request):
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
