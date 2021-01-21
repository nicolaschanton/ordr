# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters, mixins, generics
from django.db.models import Q
from datetime import datetime, timedelta
import sys
from .serializers import MainOrderSerializer

from .models import CustomerOrder
from customer_credit_card.models import CustomerCard
from utils.stripe_utils import create_charge, create_refund
from utils.customer_order_utils import create_customer_invoice
from customer_charge.models import CustomerCharge


class CustomerOrderViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.all()

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
            serializer = MainOrderSerializer

        elif self.action in ['list_public', 'retrieve_public', 'partial_update_public', 'update_public',
                             'delete_public']:
            serializer = MainOrderSerializer

        elif self.action in ['list_self', 'retrieve_self', 'partial_update_self', 'update_self', 'delete_self']:
            serializer = MainOrderSerializer

        elif self.action in ['create']:
            serializer = MainOrderSerializer

        else:
            serializer = MainOrderSerializer

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

            serializer = self.get_serializer(self.get_queryset().filter(order_state=self.request.query_params['order_state']).order_by('-order_date'), many=True)
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

                if self.get_object().order_state in ['pa', 'pr']:

                    # Workflow for Update from Paid to Preparation
                    if request.data['order_state'] == 'pr' and self.get_object().order_state == 'pa':
                        serializer.save()

                        #### TO UPDATE ####


                        # Email to customer


                        # Update Started Preparation Time
                        order = self.get_object()
                        order.order_started_preparation_date = datetime.now()
                        order.save()

                        return Response(status=status.HTTP_200_OK, data=serializer.data)

                    # Workflow for Update from Preparation to Done
                    elif request.data['order_state'] == 'do' and self.get_object().order_state == 'pr':
                        serializer.save()

                        #### TO UPDATE ####

                        # Email to customer


                        # Update Ended Preparation Time
                        order = self.get_object()
                        order.order_ended_preparation_date = datetime.now()
                        order.save()
                        return Response(status=status.HTTP_200_OK, data=serializer.data)

                    # Workflow for Update from Paid to Refused
                    elif request.data['order_state'] == 're' and self.get_object().order_state in ['pa']:
                        serializer.save()

                        #### TO UPDATE ####

                        # Email to customer

                        # Update Ended Preparation Time
                        order = self.get_object()
                        order.order_refused_date = datetime.now()
                        order.save()
                        return Response(status=status.HTTP_200_OK, data=serializer.data)

                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "order status error, probably already updated, cannot be updated"})
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "order already finished, cannot be updated!"})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            print("ERROR: " + str(sys.exc_info()))
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "bad request"})
