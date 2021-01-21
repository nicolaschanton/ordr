# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerChargeViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'customer-charges', CustomerChargeViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
