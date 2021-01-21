# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import create_customer_invoice_pdf
from .stripe_utils import st_wh_confirm_payment, st_wh_customer_creation, create_order_from_basket


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path(
        'create_customer_order/<sharable_order_id>/customer_invoice/<sharable_invoice_id>/',
        create_customer_invoice_pdf,
        name='create_customer_invoice_pdf'
    ),
    path('stripe/customer_created/', st_wh_customer_creation, name='st_wh_customer_creation'),
    path('stripe/stripe_session_completed/', st_wh_confirm_payment, name='st_wh_confirm_payment'),
    path('orders/create_order_from_basket/', create_order_from_basket, name='create_order_from_basket'),
]
