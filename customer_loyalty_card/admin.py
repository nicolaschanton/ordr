# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import CustomerLoyaltyCard, CustomerLoyaltyCardHistory


@admin.register(CustomerLoyaltyCard)
class CustomerLoyaltyCardAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = []
    list_display = [
        "id",
    ]
    pass


@admin.register(CustomerLoyaltyCardHistory)
class CustomerLoyaltyCardHistoryAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = []
    list_display = [
        "id",
    ]
    pass

