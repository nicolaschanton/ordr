# coding: utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.template import loader
import copy, json, datetime
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import requests
from rq import Queue
import random
from twilio.rest import Client
import emoji
from django.db.models import Q
from django.db.models import Count
from django.contrib.postgres import search
import sys
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import cloudinary
from django.db.models import Avg, Sum, Max, Min
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from merchant.models import Merchant
from merchant_table.models import MerchantTable
from merchant_invoice.models import MerchantInvoice
from merchant_item.models import MerchantItem
from merchant_item_category.models import MerchantItemCategory
from merchant_item_sub_category.models import MerchantItemSubCategory
from merchant_item_customization_option.models import MerchantItemCustomizationOption
from merchant_item_customization.models import MerchantItemCustomization
from merchant_notification.models import MerchantNotification
from customer_order.models import CustomerOrder
from customer_order_line.models import CustomerOrderLine
from customer_invoice.models import CustomerInvoice
from django.db.models.functions import Extract
from utils.stripe_utils import get_stripe_session_id
from customer.models import Customer


def merchant_not_found():
    return HttpResponse('<h1>Merchant was not found</h1>', status=404)


def get_merchant_by_table_id(table_id):
    try:
        merchant = MerchantTable.objects.get(id=table_id).merchant
        return merchant
    except:
        return None


def shop(request, merchant_table_id):
    # CLOUDINARY CONFIG
    cloudinary.config(
        cloud_name=str(settings.CLOUDINARY_CLOUD_NAME),
        api_key=str(settings.CLOUDINARY_API_KEY),
        api_secret=str(settings.CLOUDINARY_API_SECRET)
    )
    merchant = get_merchant_by_table_id(merchant_table_id)

    if merchant:
        merch_img = merchant.presentation_image.image(
                transformation=
                [
                    {'width': 1000, 'height': 500, 'crop': "scale", "opacity": 70, "background": "black"},
                    {'overlay':
                         {
                             'font_family': "Arial",
                             'font_weight': 'bold',
                             'font_size': 100,
                             'text_align': 'center',
                             'text': str("Bienvenue\n" + merchant.name)
                         },
                        'color': "#ffffff"
                     }
                ]
            ).replace("<img src=", "").replace("/>", "").replace('"', '')

        context = {
            "merchant": merchant,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "table_merchant_id": merchant_table_id,
            "base_url": settings.BASE_URL,
            "stripe_pk": settings.STRIPE_PUBLISHABLE_KEY,
            "merchant_image": merch_img
        }

        template = loader.get_template('frontend_customer/shop.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=86400'
        return response

    else:
        return merchant_not_found()


def order(request, merchant_table_id, order_id):
    # CLOUDINARY CONFIG
    cloudinary.config(
        cloud_name=str(settings.CLOUDINARY_CLOUD_NAME),
        api_key=str(settings.CLOUDINARY_API_KEY),
        api_secret=str(settings.CLOUDINARY_API_SECRET)
    )
    merchant = get_merchant_by_table_id(merchant_table_id)
    tg_order = CustomerOrder.objects.filter(id=order_id).first()
    orders = CustomerOrder.objects.filter(
        st_customer_id=tg_order.st_customer_id,
        order_state__in=['pa', 'pr', 'do', 'er', 're', 'rf'],
        order_date__gt=datetime.datetime.fromtimestamp(
                    float((datetime.datetime.today() - datetime.timedelta(days=7)).strftime("%s"))),
        merchant=merchant,
    )

    if merchant and tg_order:
        context = {
            "merchant": merchant,
            "table_merchant_id": merchant_table_id,
            "order": tg_order,
            "orders": orders,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "base_url": settings.BASE_URL,
            "stripe_pk": settings.STRIPE_PUBLISHABLE_KEY,
        }

        template = loader.get_template('frontend_customer/order.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=86400'
        return response

    else:
        return merchant_not_found()


def payment_fail(request):

    context = {}

    template = loader.get_template('')
    response = HttpResponse(template.render(context, request))
    response['Cache-Control'] = 'max-age=86400'
    return response
