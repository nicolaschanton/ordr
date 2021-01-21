# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import CustomerOrderLine
from merchant_item_customization.models import MerchantItemCustomization
from django.contrib.admin.widgets import FilteredSelectMultiple


@admin.register(CustomerOrderLine)
class CustomerOrderLineAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = []
    list_display = [
        "id",
        "order",
        "item",
        "created_date",
        "modified_date",
    ]
    pass

