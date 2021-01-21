# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from .constants import *
from cloudinary.models import CloudinaryField
import datetime
import uuid


class Merchant(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Key
    user = models.OneToOneField(User, related_name='merchants', on_delete=models.CASCADE)

    # General Information
    name = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    presentation_image = CloudinaryField('image', blank=True, null=True)
    open = models.BooleanField(default=False)

    # Stripe Information
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)

    # Legal Information
    registration_number = models.CharField(max_length=14, blank=True, null=True)
    vat_number = models.CharField(max_length=500, blank=True, null=True)
    owner_name = models.CharField(max_length=500, blank=True, null=True)

    # Address Information
    address_street = models.CharField(max_length=500, blank=True, null=True)
    address_city = models.CharField(max_length=500, blank=True, null=True)
    address_zip = models.CharField(max_length=500, blank=True, null=True)

    # Subscription Information
    table_quantity = models.IntegerField(default=1)

    # SEO Information
    url_tag = models.CharField(max_length=50, unique=True, blank=True, null=True)

    # Service Information
    accept_cash = models.BooleanField(default=False)
    accept_service_bar = models.BooleanField(default=False)
    accept_service_table = models.BooleanField(default=False)

    shop_description = models.TextField(
        max_length=1000,
        default="Toujours là pour vous servir dans les meilleures conditions. ENJOY!"
    )

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        name = "No Name" if not self.name else self.name
        return str(name + " - " + str(self.id))
