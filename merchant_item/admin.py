# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import MerchantItem


@admin.register(MerchantItem)
class MerchantItemAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = [
        "merchant",
        "category",
        "status"
    ]
    list_display = [
        "id",
        "merchant",
        "name",
        "category",
        "status",
        "created_date",
        "modified_date",
    ]
    pass
