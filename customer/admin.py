# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = []
    list_filter = []
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "created_date",
        "modified_date",
    ]
    pass