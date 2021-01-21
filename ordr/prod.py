from ordr.base import *
import os
import datetime


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Hosts
ALLOWED_HOSTS = [os.environ["ALLOWED_HOSTS"]]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["DB_NAME"],
        'USER': os.environ["DB_USER"],
        'PASSWORD': os.environ["DB_PASSWORD"],
        'HOST': os.environ["DB_HOST"],
        'PORT': os.environ["DB_PORT"],
    }
}


# TWILIO CONFIGURATION
# TWILIO_SID = os.environ['TWILIO_SID']
# TWILIO_TOKEN = os.environ['TWILIO_TOKEN']
# TWILIO_PHONE = os.environ['TWILIO_PHONE']
# TWILIO_PHONE_PLAIN = os.environ['TWILIO_PHONE_PLAIN']


# BASE URL
BASE_URL = os.environ["BASE_URL"]

# CLOUDINARY
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ["CLOUDINARY_CLOUD_NAME"],
    "API_KEY": os.environ["CLOUDINARY_API_KEY"],
    "API_SECRET": os.environ["CLOUDINARY_API_SECRET"]
}

CLOUDINARY_CLOUD_NAME = os.environ["CLOUDINARY_CLOUD_NAME"]
CLOUDINARY_API_KEY = os.environ["CLOUDINARY_API_KEY"]
CLOUDINARY_API_SECRET = os.environ["CLOUDINARY_API_SECRET"]


# EMAIL CONFIGURATION
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
SENDGRID_SANDBOX_MODE_IN_DEBUG = False


# STRIPE CONFIGURATION
STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']

# STRIP ENDPOINTS
STRIPE_WHS_PAYMENT_SUCCESS = os.environ['STRIPE_WHS_PAYMENT_SUCCESS']
STRIPE_WHS_CUSTOMER_CREATION = os.environ['STRIPE_WHS_CUSTOMER_CREATION']
