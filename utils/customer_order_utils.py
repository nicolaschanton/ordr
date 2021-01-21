# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.template import loader
from django.conf import settings
from twilio.rest import Client
import emoji
from datetime import datetime, timedelta
import random
import sys
import uuid
from django.db.models import Avg, Count, Min, Sum
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import csv
from io import StringIO
import zipfile37
import re
import os
import pdfkit
from django.core.files import File
import requests
from django.conf import settings

from merchant.models import Merchant
from customer.models import Customer
from merchant_table.models import MerchantTable
from customer_order.models import CustomerOrder
from user.models import User
from customer_order_line.models import CustomerOrderLine
from customer_invoice.models import CustomerInvoice
from customer_charge.models import CustomerCharge
from utils.models import SmsHistory


# from utils.order_utils import *
def get_latest_order(customer, merchant, table, order_state):
    try:
        order = CustomerOrder.objects.filter(
            customer=customer,
            merchant=merchant,
            merchant_table=table,
            order_state=order_state,
            created_date__gt=datetime.fromtimestamp(float((datetime.today() - timedelta(hours=1)).strftime("%s"))),
        ).order_by('-created_date').first()

    except:
        order = None
    return order


def update_order_financial(order):
    order_lines = CustomerOrderLine.objects.filter(order=order)
    vat_rates = []

    for order_line in order_lines:
        if order_line.vat_rate not in vat_rates:
            vat_rates.append(order_line.vat_rate)

    vat_amount_1 = 0 if not len(vat_rates) > 0 else order_lines.filter(vat_rate=vat_rates[0]).aggregate(Sum("total_vat_amount")).get("total_vat_amount__sum")
    vat_amount_2 = 0 if not len(vat_rates) > 1 else order_lines.filter(vat_rate=vat_rates[1]).aggregate(Sum("total_vat_amount")).get("total_vat_amount__sum")
    vat_amount_3 = 0 if not len(vat_rates) > 2 else order_lines.filter(vat_rate=vat_rates[2]).aggregate(Sum("total_vat_amount")).get("total_vat_amount__sum")

    order.vat_amount_1 = vat_amount_1
    order.vat_amount_2 = vat_amount_2
    order.vat_amount_3 = vat_amount_3

    order.total_amount_vat_included = 0 if not order_lines else order_lines.aggregate(Sum("total_amount_vat_included")).get("total_amount_vat_included__sum")
    order.total_amount_vat_excluded = 0 if not order_lines else order_lines.aggregate(Sum("total_amount_vat_excluded")).get("total_amount_vat_excluded__sum")

    order.save()
    return


def create_customer_invoice(order, total_refund, amount_refunded_base_100):

    # Update financial details
    update_order_financial(order=order)

    if total_refund is False and amount_refunded_base_100 == 0:
        if CustomerInvoice.objects.filter(order=order, invoice_paid=True).count() == 0:

            # Create the customer invoice instance
            customer_invoice = CustomerInvoice(
                order=order,
                invoice_date=datetime.today(),
                invoice_street=order.merchant.address_street if not order.customer.address_street else order.customer.address_street,
                invoice_city=order.merchant.address_city if not order.customer.address_city else order.customer.address_city,
                invoice_zip=order.merchant.address_zip if not order.customer.address_zip else order.customer.address_zip,
                invoice_company_name=order.merchant.name,
                invoice_customer_name=order.customer.full_name(),
                invoice_paid=True,
                invoice_vat_amount_1=order.vat_amount_1,
                invoice_vat_amount_2=order.vat_amount_2,
                invoice_vat_amount_3=order.vat_amount_3,
                invoice_total_amount_vat_included=order.total_amount_vat_included,
                invoice_total_amount_vat_excluded=order.total_amount_vat_excluded,
            )
            customer_invoice.save()

            serials = customer_invoice.get_serials()

            customer_invoice.invoice_number_text = serials[0]
            customer_invoice.invoice_number = serials[1]
            customer_invoice.save()

            # Create the PDF file
            def create_customer_invoice_pdf():
                url = str(str(settings.BASE_URL) + "/customer-order/" + str(order.id) + "/customer-invoice/" + str(customer_invoice.id) + "/")
                headers = {
                    'Content-Type': "application/json",
                    'cache-control': "no-cache",
                }
                response = requests.request("GET", url, headers=headers)
                return response

            # Possibility to enqueue this function for optimization
            pdf_file_response = create_customer_invoice_pdf()

            # Update customer invoice file
            customer_invoice.invoice_file = pdf_file_response
            customer_invoice.save()

            return customer_invoice

    elif total_refund is True and amount_refunded_base_100 > 0:
        if CustomerInvoice.objects.filter(
                order=order,
                invoice_paid=True,
                invoice_total_amount_vat_included=order.total_amount_vat_included).count() == 0:

            # Create the customer refund invoice instance
            customer_invoice = CustomerInvoice(
                order=order,
                invoice_date=datetime.today(),
                invoice_street=order.merchant.address_street if not order.customer.address_street else order.customer.address_street,
                invoice_city=order.merchant.address_city if not order.customer.address_city else order.customer.address_city,
                invoice_zip=order.merchant.address_zip if not order.customer.address_zip else order.customer.address_zip,
                invoice_company_name=order.merchant.name,
                invoice_customer_name=order.customer.full_name(),
                invoice_paid=True,
                invoice_vat_amount_1=-order.vat_amount_1,
                invoice_vat_amount_2=-order.vat_amount_2,
                invoice_vat_amount_3=-order.vat_amount_3,
                invoice_total_amount_vat_included=-order.total_amount_vat_included,
                invoice_total_amount_vat_excluded=-order.total_amount_vat_excluded,
            )
            customer_invoice.save()

            serials = customer_invoice.get_serials()

            customer_invoice.invoice_number_text = serials[0]
            customer_invoice.invoice_number = serials[1]
            customer_invoice.save()

            # Create the PDF file
            def create_customer_invoice_pdf():
                url = str(str(settings.BASE_URL) + "/customer-order/" + str(order.id) + "/customer-invoice/" + str(customer_invoice.id) + "/")
                headers = {
                    'Content-Type': "application/json",
                    'cache-control': "no-cache",
                }
                response = requests.request("GET", url, headers=headers)
                return response

            # Possibility to enqueue this function for optimization
            pdf_file_response = create_customer_invoice_pdf()

            # Update customer invoice file
            customer_invoice.invoice_file = pdf_file_response
            customer_invoice.save()

            return customer_invoice


# Script for cron checking customer order to transform in invoice or refund
def execute_create_customer_invoice():
    for order in CustomerOrder.objects.filter():
        print(order)
    return
