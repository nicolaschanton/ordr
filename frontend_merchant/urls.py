# -*- coding: utf-8 -*-

from django.urls import path, include
from .views import home, orders, merchant_login, merchant_logout, ordr_invoices, customer_orders_done, \
    customer_canceled_orders, menu_articles, menu_article_categories, menu_article_sub_categories, \
    merchant_tables, merchant_info

urlpatterns = [
    path('login/', merchant_login, name='merchant_login'),
    path('logout/', merchant_logout, name='merchant_logout'),
    path('home/', home, name='home'),
    path('orders/', orders, name='orders'),
    path('customer_canceled_orders/', customer_canceled_orders, name='customer_canceled_orders'),
    path('customer_orders_done/', customer_orders_done, name='customer_orders_done'),
    path('menu_articles/', menu_articles, name='menu_articles'),
    path('menu_article_categories/', menu_article_categories, name='menu_article_categories'),
    path('menu_article_sub_categories/', menu_article_sub_categories, name='menu_article_sub_categories'),
    path('merchant_info/', merchant_info, name='merchant_info'),
    path('merchant_tables/', merchant_tables, name='merchant_tables'),
    path('ordr_invoices/', ordr_invoices, name='ordr_invoices'),
]
