# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from .constants import *
from merchant.models import Merchant
from merchant_item_category.models import MerchantItemCategory


class MerchantItem(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    merchant = models.ForeignKey(Merchant, related_name='merchant_items', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(MerchantItemCategory, related_name='merchant_items', on_delete=models.DO_NOTHING)

    # General Information
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    price_vat_included = models.FloatField(default=0)
    price_vat_excluded = models.FloatField(default=0)
    vat_rate = models.FloatField(default=0.2)
    vat_amount = models.FloatField(default=0)
    article_image = CloudinaryField('image', blank=True, null=True)

    # Status Information
    status = models.CharField(max_length=2, choices=(
        (MENU_ITEM_ACTIVE, 'Active'),
        (MENU_ITEM_TO_BE_REVIEWED, 'To be reviewed by admin'),
        (MENU_ITEM_UNAVAILABLE, 'Unavailable'),
        (MENU_ITEM_DELETED, 'Deleted'),
    ), default=MENU_ITEM_TO_BE_REVIEWED)

    is_displayed_first_level = models.BooleanField(default=True)
    display_order = models.IntegerField(default=1)

    # Article Options
    has_happy_hour = models.BooleanField(default=False)
    happy_hour_start_hour = models.TimeField(blank=True, null=True)
    happy_hour_end_hour = models.TimeField(blank=True, null=True)

    # SEO Information
    url_tag = models.CharField(max_length=50, blank=True, null=True)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.merchant.name + " - " + self.name)
