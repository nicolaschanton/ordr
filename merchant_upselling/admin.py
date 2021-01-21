# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import MerchantUpselling


@admin.register(MerchantUpselling)
class MerchantUpsellingAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = [
    ]
    list_display = [
        "id",
        "item_1",
        "item_2",
        "created_date",
        "modified_date",
    ]
    pass
