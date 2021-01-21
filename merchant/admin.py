# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import Merchant


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = []
    list_display = [
        "id",
        "name",
        "email",
        "phone",
        "owner_name",
        "address_city",
        "created_date",
        "modified_date",
    ]
    pass