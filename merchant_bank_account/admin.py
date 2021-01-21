# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import MerchantBankAccount


@admin.register(MerchantBankAccount)
class MerchantBankAccountAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = []
    list_display = [
        "id",
    ]
    pass
