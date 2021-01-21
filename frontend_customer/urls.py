# -*- coding: utf-8 -*-

from django.urls import path, include
from .views import shop, order, payment_fail

urlpatterns = [
    path('<merchant_table_id>/', shop, name='shop'),
    path('<merchant_table_id>/order/<order_id>/', order, name='order'),
    path('<merchant_table_id>/order/<order_id>/payment_fail/', payment_fail, name='payment_fail'),
]
