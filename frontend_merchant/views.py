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
from .forms import LoginForm
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


def merchant_logout(request):
    logout(request)
    return redirect('merchant_login')


def merchant_login(request):
    context = {
        "login_form": LoginForm(),
    }

    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method == 'POST':
            sign_up_form = LoginForm(data=request.POST)
            if sign_up_form.is_valid():
                email = sign_up_form.cleaned_data["email"]
                password = sign_up_form.cleaned_data["password"]

                user = authenticate(username=email, password=password)

                if user and Merchant.objects.get(user=user):
                    login(request, user=user)
                    return redirect('home')
                else:
                    return redirect('merchant_login')

    template = loader.get_template('merchant/login.html')
    response = HttpResponse(template.render(context, request))
    response['Cache-Control'] = 'max-age=86400'
    return response


def home(request):
    if not request.user.is_authenticated:
        return redirect("merchant_login")
    elif Merchant.objects.filter(user=request.user).count() is not 1:
        auth.logout(request)
        return redirect("merchant_login")
    else:
        merchant = Merchant.objects.get(user=request.user)
        context = {
            "home_page": True,
            "base_url": settings.BASE_URL,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "merchant": merchant,
            "earnings": 0 if not CustomerOrder.objects.filter(
                merchant=merchant,
                order_state="do"
            ).aggregate(Sum('total_amount_vat_excluded')).get("total_amount_vat_excluded__sum") else
            CustomerOrder.objects.filter(
                merchant=merchant,
                order_state="do"
            ).aggregate(Sum('total_amount_vat_excluded')).get("total_amount_vat_excluded__sum"),
            "bookings": CustomerOrder.objects.filter(
                merchant=merchant,
                order_state="do"
            ).count(),
            "data_labels": [],
            "data_numbers": [],
        }

        template = loader.get_template('merchant/home.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=600'
        return response


def orders(request):
    if not request.user.is_authenticated:
        return redirect("merchant_login")
    elif Merchant.objects.filter(user=request.user).count() is not 1:
        auth.logout(request)
        return redirect("merchant_login")
    else:
        merchant = Merchant.objects.get(user=request.user)
        context = {
            "merchant": merchant,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "base_url": settings.BASE_URL,
            "tbv_orders": CustomerOrder.objects.filter(
                merchant=merchant,
                order_state__in=["pa"]
            ),
            "ongoing_orders": CustomerOrder.objects.filter(
                merchant=merchant,
                order_state__in=["pr"]
            ),
            "recently_completed_orders": CustomerOrder.objects.filter(
                merchant=merchant,
                order_state__in=["do"]
            )
        }

        template = loader.get_template('merchant/orders.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=1'
        return response


def ordr_invoices(request):
    if not request.user.is_authenticated:
        return redirect("merchant_login")
    elif Merchant.objects.filter(user=request.user).count() is not 1:
        auth.logout(request)
        return redirect("merchant_login")

    else:
        merchant = Merchant.objects.get(user=request.user)
        context = {
            "merchant": merchant,
            "base_url": settings.BASE_URL,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "ordr_invoices": MerchantInvoice.objects.filter(
                merchant=merchant,
            ).order_by("-invoice_date"),
        }

        template = loader.get_template('merchant/ordr_invoices.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=1'
        return response


def customer_orders_done(request):
    if not request.user.is_authenticated:
        return redirect("merchant_login")
    elif Merchant.objects.filter(user=request.user).count() is not 1:
        auth.logout(request)
        return redirect("merchant_login")

    else:
        try:
            searched_month = request.GET['month']
        except:
            searched_month = datetime.datetime.now().month

        try:
            searched_year = request.GET['year']
        except:
            searched_year = datetime.datetime.now().year

        merchant = Merchant.objects.get(user=request.user)
        customer_orders_qs = CustomerOrder.objects.annotate(
            order_date__month=Extract('order_date', 'month'),
            order_date__year=Extract('order_date', 'year'),
        )

        period_tuple = []
        i = 0
        date = datetime.datetime.now()
        while i < 6:
            if i == 0:
                date = date.replace(day=1) - datetime.timedelta(days=1)
            else:
                date = date.replace(day=1) - datetime.timedelta(days=1)

            period_tuple.append((date.month, date.year))
            i += 1

        context = {
            "merchant": merchant,
            "base_url": settings.BASE_URL,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "current_month": int(datetime.datetime.now().month),
            "current_year": int(datetime.datetime.now().year),
            "selected_month": int(searched_month),
            "selected_year": int(searched_year),
            "period_tuple": period_tuple,
            "customer_orders_done": customer_orders_qs.filter(
                order_state='do',
                order_date__month=searched_month,
                order_date__year=searched_year,
            ).order_by("-order_date")[:100],
        }

        template = loader.get_template('merchant/customer_orders_done.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=1'
        return response


def customer_canceled_orders(request):
    if not request.user.is_authenticated:
        return redirect("merchant_login")
    elif Merchant.objects.filter(user=request.user).count() is not 1:
        auth.logout(request)
        return redirect("merchant_login")

    else:
        try:
            searched_month = request.GET['month']
        except:
            searched_month = datetime.datetime.now().month

        try:
            searched_year = request.GET['year']
        except:
            searched_year = datetime.datetime.now().year

        merchant = Merchant.objects.get(user=request.user)
        customer_orders_qs = CustomerOrder.objects.annotate(
            order_date__month=Extract('order_date', 'month'),
            order_date__year=Extract('order_date', 'year'),
        )

        period_tuple = []
        i = 0
        date = datetime.datetime.now()
        while i < 6:
            if i == 0:
                date = date.replace(day=1) - datetime.timedelta(days=1)
            else:
                date = date.replace(day=1) - datetime.timedelta(days=1)

            period_tuple.append((date.month, date.year))
            i += 1

        context = {
            "merchant": merchant,
            "base_url": settings.BASE_URL,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "current_month": int(datetime.datetime.now().month),
            "current_year": int(datetime.datetime.now().year),
            "selected_month": int(searched_month),
            "selected_year": int(searched_year),
            "period_tuple": period_tuple,
            "customer_orders": customer_orders_qs.filter(
                order_date__month=searched_month,
                order_date__year=searched_year,
                order_state__in=["er", "re", "rf"],
            ).order_by("-order_date")[:100],
        }

        template = loader.get_template('merchant/customer_canceled_orders.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=1'
        return response


def menu_articles(request):
    if not request.user.is_authenticated:
        return redirect("merchant_login")
    elif Merchant.objects.filter(user=request.user).count() is not 1:
        auth.logout(request)
        return redirect("merchant_login")

    else:
        merchant = Merchant.objects.get(user=request.user)

        try:
            searched_category = request.GET['category']
        except:
            searched_category = '' if not MerchantItemCategory.objects.filter(
                merchant=merchant
            ).order_by("display_order").first() else MerchantItemCategory.objects.filter(
                merchant=merchant
            ).order_by("display_order").first().name

        context = {
            "merchant": merchant,
            "base_url": settings.BASE_URL,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "searched_category": searched_category,
            "categories": MerchantItemCategory.objects.filter(
                merchant=merchant).order_by("display_order"),
            "sub_categories": MerchantItemSubCategory.objects.filter(
                merchant=merchant).order_by("display_order"),
            "merchant_items": MerchantItem.objects.filter(
                merchant=merchant,
                category=MerchantItemCategory.objects.filter(
                    merchant=merchant,
                    name__contains=searched_category,
                ).order_by("display_order").first(),
            ),
        }

        template = loader.get_template('merchant/menu_articles.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=1'
        return response


def menu_article_categories(request):
    if not request.user.is_authenticated:
        return redirect("merchant_login")
    elif Merchant.objects.filter(user=request.user).count() is not 1:
        auth.logout(request)
        return redirect("merchant_login")

    else:
        merchant = Merchant.objects.get(user=request.user)
        context = {
            "merchant": merchant,
            "base_url": settings.BASE_URL,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "categories": MerchantItemCategory.objects.filter(
                merchant=merchant
            ).order_by("display_order"),
        }

        template = loader.get_template('merchant/menu_article_categories.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=1'
        return response


def merchant_tables(request):
    if not request.user.is_authenticated:
        return redirect("merchant_login")
    elif Merchant.objects.filter(user=request.user).count() is not 1:
        auth.logout(request)
        return redirect("merchant_login")

    else:
        # CLOUDINARY CONFIG
        cloudinary.config(
            cloud_name=str(settings.CLOUDINARY_CLOUD_NAME),
            api_key=str(settings.CLOUDINARY_API_KEY),
            api_secret=str(settings.CLOUDINARY_API_SECRET)
        )

        merchant = Merchant.objects.get(user=request.user)

        merchant_tables = []
        for m_table in MerchantTable.objects.filter(
                merchant=merchant,
        ).order_by("table_number"):
            t_orders = CustomerOrder.objects.filter(merchant_table=m_table, order_state='do')
            orders_count = t_orders.count()
            orders_turnover = 0 if not t_orders.aggregate(Sum('total_amount_vat_included')).get("total_amount_vat_included__sum") else t_orders.aggregate(Sum('total_amount_vat_included')).get("total_amount_vat_included__sum")

            merchant_tables.append(
                (
                    m_table.table_number,
                    orders_count,
                    orders_turnover,
                    '' if not m_table.qr_code_image else m_table.qr_code_image.url
                )
            )

        context = {
            "merchant": merchant,
            "merchant_tables": merchant_tables,
            "base_url": settings.BASE_URL,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
        }

        template = loader.get_template('merchant/merchant_tables.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=1'
        return response


def merchant_info(request):
    if not request.user.is_authenticated:
        return redirect("merchant_login")
    elif Merchant.objects.filter(user=request.user).count() is not 1:
        auth.logout(request)
        return redirect("merchant_login")
    else:
        merchant = Merchant.objects.get(user=request.user)
        context = {
            "merchant": merchant,
            "base_url": settings.BASE_URL,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
        }

        template = loader.get_template('merchant/merchant_info.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=600'
        return response


def menu_article_sub_categories(request):
    if not request.user.is_authenticated:
        return redirect("merchant_login")
    elif Merchant.objects.filter(user=request.user).count() is not 1:
        auth.logout(request)
        return redirect("merchant_login")

    else:
        merchant = Merchant.objects.get(user=request.user)

        try:
            searched_category = request.GET['category']
        except:
            searched_category = '' if not MerchantItemCategory.objects.filter(
                merchant=merchant
            ).order_by("display_order").first() else MerchantItemCategory.objects.filter(
                merchant=merchant
            ).order_by("display_order").first().name

        context = {
            "merchant": merchant,
            "base_url": settings.BASE_URL,
            "cloudinary_cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "searched_category": searched_category,
            "categories": MerchantItemCategory.objects.filter(
                merchant=merchant).order_by("display_order"),
            "sub_categories": MerchantItemSubCategory.objects.filter(
                merchant=merchant,
                category__name=searched_category
            ).order_by("display_order"),
        }

        template = loader.get_template('merchant/menu_article_sub_categories.html')
        response = HttpResponse(template.render(context, request))
        response['Cache-Control'] = 'max-age=1'
        return response
