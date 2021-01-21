# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from customer.models import Customer
from .constants import *


class CustomerCard(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

    # Status Info
    status = models.CharField(
        max_length=2,
        choices=(
            (STATUS_ACTIVE, 'Active'),
            (STATUS_INACTIVE, 'Inactive'),
            (STATUS_DELETED, 'Deleted'),
        ),
        default=STATUS_ACTIVE,
    )

    # Stripe Info
    stripe_card_id = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    cvc_check = models.CharField(max_length=100, blank=True, null=True)
    dynamic_last4 = models.CharField(max_length=100, blank=True, null=True)
    exp_month = models.IntegerField(default=1)
    exp_year = models.IntegerField(default=2019)
    fingerprint = models.CharField(max_length=100, blank=True, null=True)
    funding = models.CharField(max_length=100, blank=True, null=True)
    last4 = models.CharField(max_length=100, blank=True, null=True)
    metadata = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    tokenization_method = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.stripe_card_id)
