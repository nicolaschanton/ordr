# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from .constants import *
from customer.models import Customer
from customer_credit_card.models import CustomerCard
from merchant.models import Merchant
from merchant_table.models import MerchantTable


class CustomerOrder(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING)
    merchant_table = models.ForeignKey(MerchantTable, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, blank=True, null=True)
    customer_card = models.ForeignKey(CustomerCard, on_delete=models.DO_NOTHING, blank=True, null=True)

    # General Information
    order_state = models.CharField(
        max_length=2,
        choices=(
            (STATUS_DRAFT, 'Draft'),
            (STATUS_PAID, 'Paid'),
            (STATUS_PREPARATION, 'In Preparation'),
            (STATUS_DONE, 'Done'),
            (STATUS_ERROR_PAYMENT, 'Payment Error'),
            (STATUS_REFUSED, 'Refused'),
            (STATUS_REFUNDED, 'Refunded'),
            (STATUS_DELETED, 'Deleted'),
            (STATUS_COMPLETED, 'Completed')
        ),
        default=STATUS_DRAFT,
    )
    order_date = models.DateTimeField(blank=True, null=True)
    order_paid_date = models.DateTimeField(blank=True, null=True)
    order_started_preparation_date = models.DateTimeField(blank=True, null=True)
    order_ended_preparation_date = models.DateTimeField(blank=True, null=True)
    order_refused_date = models.DateTimeField(blank=True, null=True)
    order_refunded_date = models.DateTimeField(blank=True, null=True)

    # Stripe Information
    st_checkout_session_id = models.CharField(max_length=250, blank=True, null=True)
    st_customer_id = models.CharField(max_length=250, blank=True, null=True)

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
        return str(self.merchant.name + " - " + str(self.id))
