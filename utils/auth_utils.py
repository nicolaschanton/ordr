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
from .models import PhoneValidation


# from utils.auth_utils import *
def get_phone_validation_code(phone):
    # Create Validation Code
    validation_code = random.randint(100000, 999999)

    # Save Validation Code
    phone_validation = PhoneValidation(
        code=validation_code,
        phone=phone,
    )
    phone_validation.save()

    return str(validation_code)


def is_phone_validation_code_ok(phone, code):

    phone_validation = PhoneValidation.objects.filter(
        phone=phone,
        code=code,
        created_date__gte=datetime.fromtimestamp(float((datetime.today() - timedelta(minutes=10)).strftime("%s"))),
    ).order_by("-created_date")

    if phone_validation.count() == 1:
        result = True

    else:
        result = False

    return result


def create_password_from_phone_validation(phone, code):

    string_1 = "#45£*$469$%HG§@dd$sf@"
    string_2 = "$46@dd$£sf@9$#45*%HG§"
    string_3 = "#4HG§@dd$sf@_5*$4Hf@6_9$%ç£"
    string_4 = "#45*@dd$sf@"
    string_5 = str(code[:3])
    string_6 = str(code[3:])
    string_7 = str(phone)

    password = str(string_1 + string_4 + string_3 + string_7 + string_2 + string_6 + string_5)

    return password
