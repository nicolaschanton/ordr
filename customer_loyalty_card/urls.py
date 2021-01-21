# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerLoyaltyCardViewSet, CustomerLoyaltyCardHistoryViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'customer-loyalty-cards', CustomerLoyaltyCardViewSet)
router.register(r'customer-loyalty-cards-histories', CustomerLoyaltyCardHistoryViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
