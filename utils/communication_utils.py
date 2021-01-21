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
from .utils import first_day_of_month, last_day_of_month


# from utils.communication_utils import *
def send_sms(to, message_body, sms_type):

    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = str(settings.TWILIO_SID)
    auth_token = str(settings.TWILIO_TOKEN)
    client = Client(account_sid, auth_token)
    from_phone = str(settings.TWILIO_PHONE)

    try:
        message = client.messages.create(
            str(to),
            body=message_body,
            from_=from_phone
        )

        print("SUCCESS: SMS PROPERLY SENT - ", to, message.sid, message.date_created.date, message.body)

        SmsHistory(
            content=message.body,
            sms_type=sms_type,
        ).save()

    except:
        print("ERROR: Twilio API Error - Message not sent " + " - " + str(sys.exc_info()))

    return


def send_email(to_address, from_address, subject, template_path, context_dict):
    try:
        msg = EmailMessage(
            str(subject),
            str(render_to_string(str(template_path), context_dict)),
            from_address,
            [to_address],
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

    except:
        print(sys.exc_info())
    return


def send_customer_invoices_to_merchant(inv_merchant, inv_month, inv_year):
    date = datetime.today().replace(month=inv_month, year=inv_year)

    customer_invoices = CustomerInvoice.objects.filter(
        order__merchant=inv_merchant,
        invoice_file__isnull=False,
        invoice_date__gte=first_day_of_month(date=date),
        invoice_date__lte=last_day_of_month(date=date),
        invoice_paid=True,
    )

    # Create the CSV accounting recap file
    csvfile = StringIO()

    fieldnames = [
        "invoice_number_text",
        "invoice_date",
        "invoice_vat_amount_1",
        "invoice_vat_amount_2",
        "invoice_vat_amount_3",
        "invoice_total_amount_vat_included",
        "invoice_total_amount_vat_excluded",
        "invoice_url"
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for invoice in customer_invoices:
        writer.writerow(
            {
                "invoice_number_text": invoice.invoice_number_text,
                "invoice_date": invoice.invoice_date.strftime("%Y/%m/%d"),
                "invoice_vat_amount_1": invoice.invoice_vat_amount_1,
                "invoice_vat_amount_2": invoice.invoice_vat_amount_2,
                "invoice_vat_amount_3": invoice.invoice_vat_amount_3,
                "invoice_total_amount_vat_included": invoice.invoice_total_amount_vat_included,
                "invoice_total_amount_vat_excluded": invoice.invoice_total_amount_vat_excluded,
                "invoice_url": invoice.invoice_file.url
            }
        )

    # Create the ZIP file of all the invoices for this merchant / month / year


    # Send the Email
    email = EmailMessage(
        str('[IMPORTANT] Export comptable des factures clients - ' + str(inv_month) + "/" + str(inv_year)),
        '',
        os.environ["EMAIL_ADMIN"],
        [str(inv_merchant.email), "nicolas.chanton@gmail.com"],
    )
    email.attach(str('export_invoices_' + str(inv_month) + "-" + str(inv_year) + '.csv'), csvfile.getvalue(), 'text/csv')

    # from project_x_api.utils import *
    # send_customer_invoices_to_merchant(inv_merchant=Merchant.objects.filter().first(), inv_month=8, inv_year=2019)

    email.send()

    return
