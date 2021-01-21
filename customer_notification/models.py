# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime
import uuid
from customer.models import Customer


class CustomerNotification(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

    # General Info
    title = models.CharField(max_length=500)
    message = models.CharField(max_length=500)
    read = models.BooleanField(default=False)

    # Auto Timestamp Generation
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
