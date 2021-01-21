# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from merchant.models import Merchant


class MerchantBankAccount(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    merchant = models.OneToOneField(Merchant, on_delete=models.DO_NOTHING)

    # Bank Account Information
    bank_iban = models.CharField(max_length=500, blank=True, null=True)
    account_holder_name = models.CharField(max_length=500, blank=True, null=True)

    # Stripe Info
    stripe_bank_account_id = models.CharField(max_length=500, blank=True, null=True)
    client_secret = models.CharField(max_length=500, blank=True, null=True)
    currency = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=500, blank=True, null=True)
    usage = models.CharField(max_length=500, blank=True, null=True)
    sd_bank_code = models.CharField(max_length=500, blank=True, null=True)
    sd_country = models.CharField(max_length=500, blank=True, null=True)
    sd_fingerprint = models.CharField(max_length=500, blank=True, null=True)
    sd_last4 = models.CharField(max_length=500, blank=True, null=True)
    sd_mandate_reference = models.CharField(max_length=500, blank=True, null=True)
    sd_mandate_url = models.CharField(max_length=500, blank=True, null=True)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.merchant.name + " - " + str(self.id))
