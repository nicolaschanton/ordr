# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from merchant.models import Merchant
from .constants import *


class MerchantLoyaltyProgram(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING)

    # General Information
    spending_to_point_conversion = models.FloatField(default=0)
    point_to_reward_conversion = models.FloatField(default=0)
    point_lifespan_days = models.IntegerField(default=365)

    # Status Information
    status = models.CharField(max_length=3, choices=(
        (MENU_ITEM_ACTIVE, 'Active'),
        (MENU_ITEM_TO_BE_REVIEWED, 'To be reviewed by admin'),
        (MENU_ITEM_UNAVAILABLE, 'Unavailable'),
        (MENU_ITEM_DELETED, 'Deleted'),
    ), default=MENU_ITEM_TO_BE_REVIEWED)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.merchant.name
