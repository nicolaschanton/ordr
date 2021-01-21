# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import MerchantItemCustomization


@admin.register(MerchantItemCustomization)
class MerchantItemCustomizationAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = []
    list_display = [
        "id",
        "name",
        "item",
        "status",
        "created_date",
        "modified_date",
    ]
    pass
