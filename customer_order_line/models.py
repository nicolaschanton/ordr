# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from customer_order.models import CustomerOrder
from merchant_item.models import MerchantItem
from merchant_item_customization.models import MerchantItemCustomization
from merchant_item_customization_option.models import MerchantItemCustomizationOption


class CustomerOrderLine(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    order = models.ForeignKey(CustomerOrder, on_delete=models.DO_NOTHING, related_name='customer_order_lines')
    item = models.ForeignKey(MerchantItem, on_delete=models.DO_NOTHING, related_name='customer_order_lines')
    parent_order_line_id = models.UUIDField(primary_key=False, blank=True, null=True, editable=True)

    # General Information
    label = models.CharField(max_length=100)
    quantity = models.FloatField(default=1)
    ready = models.BooleanField(default=False)

    # Financial Information
    unit_amount_vat_included = models.FloatField(default=0)
    unit_amount_vat_excluded = models.FloatField(default=0)
    unit_vat_amount = models.FloatField(default=0)
    vat_rate = models.FloatField(default=0.2)
    total_amount_vat_included = models.FloatField(default=0)
    total_amount_vat_excluded = models.FloatField(default=0)
    total_vat_amount = models.FloatField(default=0)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item.name
