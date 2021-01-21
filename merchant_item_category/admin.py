# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import MerchantItemCategory


@admin.register(MerchantItemCategory)
class MerchantItemCategoryAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = [
        "merchant",
        "status",
    ]
    list_display = [
        "id",
        "name",
        "merchant",
        "status",
        "created_date",
        "modified_date",
    ]
    pass


