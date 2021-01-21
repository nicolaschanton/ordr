# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import CustomerInvoice


@admin.register(CustomerInvoice)
class CustomerInvoiceAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = [
        "invoice_date"
    ]
    list_display = [
        "id",
        "invoice_number_text",
        "invoice_date",
        "created_date",
        "modified_date",
    ]
    pass