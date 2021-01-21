# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import CustomerOrder


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = [
        "merchant",
        "order_state"
    ]
    list_display = [
        "id",
        "order_state",
        "created_date",
        "modified_date",
    ]
    pass