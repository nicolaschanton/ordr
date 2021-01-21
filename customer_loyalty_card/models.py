# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from customer.models import Customer
from merchant_loyalty_program.models import MerchantLoyaltyProgram
from django.utils.timezone import now


class CustomerLoyaltyCard(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    loyalty_program = models.ForeignKey(MerchantLoyaltyProgram, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

    # General Information
    point_count = models.FloatField(default=0)

    # Status Information
    deleted = models.BooleanField(default=False)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(str(self.customer.id) + " - " + self.loyalty_program.merchant.name)


class CustomerLoyaltyCardHistory(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    customer_loyalty_card = models.ForeignKey(CustomerLoyaltyCard, related_name='customer_loyalty_card_histories', on_delete=models.DO_NOTHING)

    # General Information
    point_modification = models.FloatField(default=0)
    point_modification_date = models.DateTimeField(default=now)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(str(self.customer_loyalty_card.customer.id) + " - " + self.customer_loyalty_card.loyalty_program.merchant.name)
