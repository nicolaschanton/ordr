# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from merchant.models import Merchant
from merchant_order.models import MerchantOrder


class MerchantInvoice(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING)
    merchant_order = models.ForeignKey(MerchantOrder, on_delete=models.DO_NOTHING)

    # General Information
    invoice_number = models.IntegerField(default=1)
    invoice_number_text = models.CharField(max_length=100)
    invoice_date = models.DateField(default=datetime.date.today)
    invoice_street = models.CharField(max_length=500)
    invoice_city = models.CharField(max_length=500)
    invoice_zip = models.CharField(max_length=500)
    invoice_vat_rate = models.FloatField(default=0.2)
    invoice_vat_amount = models.FloatField(default=0)
    invoice_total_amount_vat_included = models.FloatField(default=0)
    invoice_total_amount_vat_excluded = models.FloatField(default=0)
    invoice_company_name = models.CharField(max_length=500)
    invoice_contact_name = models.CharField(max_length=500)
    invoice_paid = models.BooleanField(default=False)
    invoice_pdf = CloudinaryField('file', blank=True, null=True)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number_text

    def get_serials(self):
        if not self.invoice_number_text:
            starting_day_of_current_year = self.invoice_date.replace(month=1, day=1)
            ending_day_of_current_year = self.invoice_date.replace(month=12, day=31)

            max_nb = MerchantInvoice.objects.filter(
                invoice_date__gt=starting_day_of_current_year,
                invoice_date__lt=ending_day_of_current_year,
                merchant=self.merchant,
                invoice_number__isnull=False,
            ).order_by("-invoice_date").first().invoice_number + 1

            serial_number = format(int(max_nb) / 10000000, '.7f')[2:]
            serial_text = str(
                str("FMERCH-")
                + str(self.merchant.url_tag.upper())
                + str("-")
                + str(self.invoice_date.year)
                + str(serial_number)
            )
        else:
            serial_text = self.invoice_number_text
            serial_number = self.invoice_number

        return serial_text, serial_number
