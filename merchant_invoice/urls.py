# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MerchantInvoiceViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'merchant-invoices', MerchantInvoiceViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
