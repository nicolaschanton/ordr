# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from twilio.rest import Client
import emoji
from datetime import datetime, timedelta
from django.conf import settings
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

from merchant.models import Merchant
from customer.models import Customer
from merchant_table.models import MerchantTable
from customer_order.models import CustomerOrder
from user.models import User
from customer_order_line.models import CustomerOrderLine
from customer_invoice.models import CustomerInvoice
from customer_charge.models import CustomerCharge
from utils.models import SmsHistory


# from utils.utils import *
def is_mobile(request):
    response = False if "mobile" not in request.META['HTTP_USER_AGENT'].lower() else True
    return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    else:
        return date.replace(month=date.month + 1, day=1) - timedelta(days=1)


def first_day_of_month(date):
    return date.replace(day=1) - timedelta(days=1)
