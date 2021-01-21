# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid


class Customer(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    # user = models.OneToOneField(User, related_name='customers', on_delete=models.CASCADE)

    # General Information
    first_name = models.CharField(max_length=500, blank=True, null=True)
    last_name = models.CharField(max_length=500, blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Stripe Information
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)

    # Address Information
    address_street = models.CharField(max_length=500, blank=True, null=True)
    address_city = models.CharField(max_length=500, blank=True, null=True)
    address_zip = models.CharField(max_length=500, blank=True, null=True)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def full_name(self):
        try:
            full_name = str(self.first_name.capitalize() + " " + self.last_name.capitalize())
        except:
            full_name = str(self.id)[:10]
        return full_name

    def __str__(self):
        return str(self.id)
