# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from merchant.models import Merchant


class MerchantBillingPlan(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING)

    # Billing Plan General Information
    active = models.BooleanField(default=False)
    starting_date = models.DateField(auto_now_add=True)

    # Billing Plan Financial Information
    base_monthly_fees_vat_excluded = models.FloatField(default=0)
    base_monthly_fees_vat_included = models.FloatField(default=0)
    base_monthly_fees_vat_amount = models.FloatField(default=0)

    variable_fees_vat_excluded = models.FloatField(default=0)
    variable_fees_vat_included = models.FloatField(default=0)
    variable_fees_vat_amount = models.FloatField(default=0)

    is_indexed_on_order_number = models.BooleanField(default=False)
    is_indexed_on_order_amount = models.BooleanField(default=False)

    fees_per_order_vat_excluded = models.FloatField(default=0)
    fees_per_order_vat_included = models.FloatField(default=0)
    fees_per_order_vat_amount = models.FloatField(default=0)

    fees_per_euro_vat_excluded = models.FloatField(default=0)
    fees_per_euro_vat_included = models.FloatField(default=0)
    fees_per_euro_vat_amount = models.FloatField(default=0)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
