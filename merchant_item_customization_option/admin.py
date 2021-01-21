# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import MerchantItemCustomizationOption


@admin.register(MerchantItemCustomizationOption)
class MerchantItemCustomizationOptionAdmin(admin.ModelAdmin):
    search_fields = [
        "item_customization__name",
        "item__name"
    ]
    list_filter = [
        "item__merchant"
    ]
    list_display = [
        "id",
        "item",
        "item_customization",
        "created_date",
        "modified_date",
    ]
    pass
