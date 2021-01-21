# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from .constants import *
from merchant_item.models import MerchantItem


class MerchantItemCustomization(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    item = models.ForeignKey(MerchantItem, related_name='merchant_item_customizations', on_delete=models.DO_NOTHING)

    # General Information
    name = models.CharField(max_length=500)
    max_permitted = models.IntegerField(default=1)
    min_permitted = models.IntegerField(default=1)

    # Status Information
    status = models.CharField(max_length=2, choices=(
        (MENU_ITEM_ACTIVE, 'Active'),
        (MENU_ITEM_TO_BE_REVIEWED, 'To be reviewed by admin'),
        (MENU_ITEM_UNAVAILABLE, 'Unavailable'),
        (MENU_ITEM_DELETED, 'Deleted'),
    ), default=MENU_ITEM_TO_BE_REVIEWED)

    display_order = models.IntegerField(default=1)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item.merchant.name + " - " + self.item.name + " - " + self.name)
