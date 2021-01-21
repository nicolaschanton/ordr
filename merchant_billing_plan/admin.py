# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import MerchantBillingPlan


@admin.register(MerchantBillingPlan)
class MerchantBillingPlanAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = [
        "merchant",
    ]
    list_display = [
        "id",
        "merchant",
        "created_date",
        "modified_date",
    ]
    pass
