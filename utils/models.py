# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from customer.models import Customer
from merchant.models import Merchant


class SmsHistory(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, blank=True, null=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING, blank=True, null=True)

    # Main Information
    phone = models.CharField(max_length=15)
    message_body = models.CharField(max_length=500)
    send_date = models.DateTimeField(auto_now_add=True)

    # Notification Type
    sms_type = models.CharField(max_length=500)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone


class EmailHistory(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, blank=True, null=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING, blank=True, null=True)

    # Main Information
    email = models.EmailField(max_length=500)
    message_body = models.CharField(max_length=500)
    send_date = models.DateTimeField(auto_now_add=True)

    # Notification Type
    email_type = models.CharField(max_length=500)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class PhoneValidation(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # General Information
    code = models.CharField(max_length=6, default='564098')
    phone = models.CharField(max_length=15, default='0622695505')

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.code)
