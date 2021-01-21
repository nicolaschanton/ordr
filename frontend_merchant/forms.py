# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from django.core.validators import RegexValidator
import datetime


# LOGIN FORM
class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label="Email",
        label_suffix="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "mon_mail@mail.fr"
            }
        )
    )

    password = forms.CharField(
        required=True,
        label="Mot de Passe",
        label_suffix="",
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "********"
            }
        )
    )


# LOGIN FORM
class ContactForm(forms.Form):
    email = forms.CharField(
        required=True,
        label="Votre message",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Votre message *"
            }
        )
    )
