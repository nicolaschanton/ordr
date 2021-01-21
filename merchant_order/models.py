# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from .constants import *
from merchant.models import Merchant
from merchant_billing_plan.models import MerchantBillingPlan


class MerchantOrder(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING)
    merchant_billing_plan = models.ForeignKey(MerchantBillingPlan, on_delete=models.DO_NOTHING)

    # General Information
    order_state = models.CharField(
        max_length=2,
        choices=(
            (STATUS_DRAFT, 'Draft'),
            (STATUS_PAID, 'Paid'),
            (STATUS_ERROR_PAYMENT, 'Payment Error'),
            (STATUS_REFUNDED, 'Refunded'),
            (STATUS_DELETED, 'Deleted')
        ),
        default=STATUS_DRAFT,
    )
    order_paid_date = models.DateTimeField(blank=True, null=True)

    # Financial Information
    total_amount_vat_included = models.FloatField(default=0)
    total_amount_vat_excluded = models.FloatField(default=0)
    vat_amount_1 = models.FloatField(default=0)
    vat_amount_2 = models.FloatField(default=0)
    vat_amount_3 = models.FloatField(default=0)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.merchant.name)
