# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from merchant.models import Merchant
from merchant_bank_account.models import MerchantBankAccount
from .constants import *


class MerchantCharge(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Key
    merchant_bank_account = models.ForeignKey(MerchantBankAccount, on_delete=models.DO_NOTHING)

    # Stripe Info
    charge_id = models.CharField(max_length=500)
    amount = models.FloatField(default=0)
    amount_refunded = models.FloatField(default=0)
    currency = models.CharField(max_length=500)
    created = models.DateTimeField()

    # Status Field
    status = models.CharField(
        max_length=2,
        choices=(
            (STATUS_DRAFT, 'Draft'),
            (STATUS_SENT, 'Sent'),
            (STATUS_DONE, 'Done'),
            (STATUS_ERROR, 'Error')
        ),
        default=STATUS_DRAFT,
    )

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.merchant_bank_account.merchant.name
