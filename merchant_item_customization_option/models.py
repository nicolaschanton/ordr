# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from .constants import *
from merchant_item_customization.models import MerchantItemCustomization
from merchant_item.models import MerchantItem


class MerchantItemCustomizationOption(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    item_customization = models.ForeignKey(MerchantItemCustomization,
                                           related_name='merchant_item_customization_options',
                                           on_delete=models.DO_NOTHING)
    item = models.ForeignKey(MerchantItem, on_delete=models.DO_NOTHING, blank=True, null=True)

    # Pricing Information
    price_vat_included = models.FloatField(default=0)
    price_vat_excluded = models.FloatField(default=0)
    vat_rate = models.FloatField(default=0.2)
    vat_amount = models.FloatField(default=0)

    # General Information
    default_quantity = models.IntegerField(default=0)
    max_permitted = models.IntegerField(default=1)
    min_permitted = models.IntegerField(default=1)
    display_order = models.IntegerField(default=1)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item.merchant.name + " - " + self.item_customization.item.name + " - " + self.item.name)
