# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from .constants import *
from merchant.models import Merchant
from merchant_item.models import MerchantItem


class MerchantUpselling(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    item_1 = models.ForeignKey(MerchantItem, related_name="item_1", on_delete=models.DO_NOTHING)
    item_2 = models.ForeignKey(MerchantItem, related_name="item_2", on_delete=models.DO_NOTHING)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item_1.name + " - " + self.item_1.name)
