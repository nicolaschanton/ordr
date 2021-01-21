# -*- coding: utf-8 -*-

from merchant.models import Merchant
from customer.models import Customer
from merchant_table.models import MerchantTable
from merchant_item.models import MerchantItem
from merchant_item_customization.models import MerchantItemCustomization
from merchant_item_customization_option.models import MerchantItemCustomizationOption
from customer_order.models import CustomerOrder
from user.models import User
from customer_order_line.models import CustomerOrderLine
from customer_invoice.models import CustomerInvoice
from customer_charge.models import CustomerCharge
from customer_credit_card.models import CustomerCard
from utils.models import SmsHistory
from merchant_bank_account.models import MerchantBankAccount
from merchant_charge.models import MerchantCharge
from merchant_invoice.models import MerchantInvoice
from django.conf import settings
import requests
import os
import stripe
from .customer_order_utils import update_order_financial
import copy, json, datetime
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .customer_order_utils import update_order_financial
from django.http import JsonResponse


# Stripe Init
stripe.api_key = settings.STRIPE_SECRET_KEY


# Customer Operations
def create_customer(customer):
    response = stripe.Customer.create(
        description=customer.id,
        email=customer.email,
        metadata={
            "is_merchant": False,
            "is_customer": True
        }
    )

    customer.stripe_customer_id = response.get("id")
    customer.save()
    return response


def update_customer(customer, email, data):
    response = stripe.Customer.modify(
        str(customer.stripe_customer_id),
        email=email,
        metadata=data  # Has to be Dict
    )
    return response


def retrieve_customer(customer):
    if customer.stripe_customer_id:
        response = stripe.Customer.retrieve(customer.stripe_customer_id)
    else:
        response = None
    return response


# Merchant Operations
def create_merchant(merchant):
    response = stripe.Customer.create(
        description=merchant.id,
        email=merchant.email,
        metadata={
            "is_merchant": True,
            "is_customer": False
        }
    )

    merchant.stripe_customer_id = response.get("id")
    merchant.save()
    return response


def update_merchant(merchant, data, email):
    response = stripe.Customer.modify(
        str(merchant.stripe_customer_id),
        email=email,
        metadata=data  # Has to be Dict
    )
    return response


def retrieve_merchant(merchant):
    if merchant.stripe_customer_id:
        response = stripe.Customer.retrieve(merchant.stripe_customer_id)
    else:
        response = None
    return response


# Bank Account Operations
def create_bank_account(merchant, bank_iban, account_holder_name):
    bank_account = stripe.Source.create(
        type='sepa_debit',
        sepa_debit={'iban': str(bank_iban)},
        currency='eur',
        owner={
            'name': str(account_holder_name),
        },
    )

    # Update Merchant Bank Account
    merchant_bank_account = MerchantBankAccount(
        merchant=merchant,
        bank_iban=bank_iban,
        account_holder_name=bank_account.get("owner").get("name"),
        stripe_bank_account_id=bank_account.get("id"),
        client_secret=bank_account.get("client_secret"),
        currency=bank_account.get("currency"),
        status=bank_account.get("status"),
        type=bank_account.get("type"),
        usage=bank_account.get("usage"),
        sd_bank_code=bank_account.get("sepa_debit").get("bank_code"),
        sd_country=bank_account.get("sepa_debit").get("country"),
        sd_fingerprint=bank_account.get("sepa_debit").get("fingerprint"),
        sd_last4=bank_account.get("sepa_debit").get("last4"),
        sd_mandate_reference=bank_account.get("sepa_debit").get("mandate_reference"),
        sd_mandate_url=bank_account.get("sepa_debit").get("mandate_url"),
    )
    merchant_bank_account.save()

    return merchant_bank_account


# Credit Card Operations
def create_credit_card(customer, number, exp_month, exp_year, cvc, name, email):
    card = stripe.Customer.create_source(
        str(customer.stripe_customer_id),
        source={
            "object": "card",
            "number": str(number).replace(" ", ""),  # String no spaces
            "exp_month": int(exp_month),  # Int
            "exp_year": int(exp_year),  # Int
            "cvc": str(cvc).replace(" ", ""),  # String no spaces
            "name": str(name),  # String

        }
    )

    customer_card = CustomerCard(
        customer=customer,
        stripe_card_id=card.get("id"),
        brand=card.get("brand"),
        country=card.get("country"),
        stripe_customer_id=card.get("customer"),
        cvc_check=card.get("cvc_check"),
        dynamic_last4=card.get("dynamic_last4"),
        exp_month=card.get("exp_month"),
        fingerprint=card.get("fingerprint"),
        funding=card.get("funding"),
        last4=card.get("last4"),
        metadata=card.get("metadata"),
        name=card.get("name"),
        tokenization_method=card.get("tokenization_method"),
        email=email,
    )
    customer_card.save()

    return customer_card


def list_credit_cards(customer):
    cards = stripe.Customer.list_sources(
        str(customer.stripe_customer_id),
        limit=5,
        object='card'
    ).get("data")

    return cards


# Charge Operations
def create_charge(stripe_customer_id, immediate_capture, payment_id, amount_vat_included_base_100, order):

    merchant_bank_account = MerchantBankAccount.objects.filter(
        merchant__stripe_customer_id=stripe_customer_id,
        stripe_bank_account_id=payment_id,
    ).first()
    customer_card = CustomerCard.objects.filter(
        customer__stripe_customer_id=stripe_customer_id,
        stripe_card_id=payment_id,
    ).first()

    customer_charge = ''

    if merchant_bank_account:
        charge = stripe.Charge.create(
            amount=amount_vat_included_base_100,
            customer=stripe_customer_id,
            capture=immediate_capture,  # Boolean Field
            currency="eur",
            source=str(payment_id),
            description=str("Charge for merchant " + stripe_customer_id)
        )

        if charge.get("status") == "succeeded":
            customer_charge = MerchantCharge(
                merchant_bank_account=merchant_bank_account,
                charge_id=charge.get("id"),
                captured=charge.get("captured"),
                amount=float(charge.get("amount") / 100),
                amount_refunded=float(charge.get("amount_refunded") / 100),
                currency=charge.get("currency"),
                created=datetime.datetime.fromtimestamp(charge.get("created")),
            )
            customer_charge.save()

    elif customer_card:
        # Update the order's financial
        update_order_financial(order=order)

        charge = stripe.Charge.create(
            amount=amount_vat_included_base_100,
            customer=stripe_customer_id,
            capture=immediate_capture,  # Boolean Field
            currency="eur",
            source=str(payment_id),
            description=str("Charge for customer " + stripe_customer_id)
        )

        if charge.get("status") == "succeeded":
            customer_charge = CustomerCharge(
                customer_card=customer_card,
                order=order,
                charge_id=charge.get("id"),
                status="do" if charge.get("captured") is True else "er",
                amount=float(charge.get("amount") / 100),
                amount_refunded=float(charge.get("amount_refunded") / 100),
                currency=charge.get("currency"),
                created=datetime.datetime.fromtimestamp(charge.get("created")),
            )

            customer_charge.save()

    else:
        raise ValueError("Unknown Payment Id")

    return customer_charge


# Refunds Operations
def create_refund(charge, amount_base_100):

    # Stripe Refund
    re = stripe.Refund.create(
        charge=charge.charge_id,
        amount=int(amount_base_100)
    )

    negative_customer_charge = ''

    # Internal refund object
    if re.get("status") == "succeeded":
        negative_customer_charge = CustomerCharge(
            customer=charge.customer,
            customer_card=charge.customer_card,
            charge_id=re.get("charge"),
            captured=True,
            amount=0,
            amount_refunded=-amount_base_100,
            currency="eur",
            created=re.get("created"),
        )
        negative_customer_charge.save()

    return negative_customer_charge


# from utils.stripe_utils import *
def get_stripe_session_id(merchant_table_id, order, customer):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Update Order
    update_order_financial(order=order)

    # Build the payload for cs
    line_items_constructor = []
    for order_line in CustomerOrderLine.objects.filter(order=order):
        line_items_constructor.append(
            {
                'name': str(order_line.item.name + " X" + str(int(order_line.quantity))),
                'description': str(order_line.item.description[:50]),
                'images': [order_line.item.article_image.build_url(width=300, height=300, crop='fill')],
                'amount': int(float(order_line.total_amount_vat_included) * 100),
                'currency': 'eur',
                'quantity': 1,
            }
        )

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        success_url=str(settings.BASE_URL + "/shop/" + str(merchant_table_id) + "/order/" + str(order.id) + "/"),
        cancel_url=str(settings.BASE_URL + "/shop/" + str(merchant_table_id)),
        customer_email='' if not customer else customer.email,
        line_items=line_items_constructor,
    )

    if session['id']:
        order.st_checkout_session_id = session['id']
        order.save()

        return session['id']

    else:
        return None


@csrf_exempt
def st_wh_confirm_payment(request):
    endpoint_secret = settings.STRIPE_WHS_PAYMENT_SUCCESS
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )

    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        order = CustomerOrder.objects.filter(
            st_checkout_session_id=session.get("id")
        ).first()

        if order:
            # Update Order State to Paid
            order.order_state = 'pa'
            order.order_paid_date = datetime.datetime.now()

            # Update Stripe Customer Id in Order
            order.st_customer_id = session.get("customer")
            order.save()

            return HttpResponse(status=200)

        else:
            return HttpResponse(status=400)


@csrf_exempt
@require_POST
def st_wh_customer_creation(request):
    endpoint_secret = settings.STRIPE_WHS_PAYMENT_SUCCESS
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )

    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'customer.created':
        st_customer = event['data']['object']

        # Retrieve Orders
        orders = CustomerOrder.objects.filter(
            st_customer_id=st_customer.get("id")
        )

        # Retrieve the customer
        customer = Customer.objects.filter(
            email=st_customer.get("email"),
            stripe_customer_id=st_customer.get("id")
        ).first()

        if not customer:
            for order in orders:
                tg_customer = Customer(
                    email=st_customer.get("email"),
                    stripe_customer_id=st_customer.get("id"),
                )
                tg_customer.save()

                order.customer = tg_customer
                order.save()

            return HttpResponse(status=200)

        else:
            return HttpResponse(status=400)


@csrf_exempt
@require_POST
def create_order_from_basket(request):
    try:
        json_data = json.loads(request.body)
        table_merchant_id = json_data["table_merchant_id"]
        customer_id = json_data["customer_id"]
        basket_items = json_data["basket"]
        merchant_table = MerchantTable.objects.filter(id=table_merchant_id).first()

        try:
            customer = None if Customer.objects.filter(id=customer_id).count() == 0 else Customer.objects.get(id=customer_id)
        except:
            customer = Customer()
            customer.save()

        # Create a new order
        new_order = CustomerOrder(
            customer=customer,
            merchant=merchant_table.merchant,
            merchant_table=merchant_table,
            order_state='dr',
            order_date=datetime.datetime.now(),
        )
        new_order.save()

        # Create Order Lines attached to this Order
        for basket_item in basket_items:
            try:
                tg_item = MerchantItem.objects.get(id=basket_item["id"])

            except:
                # Invalid payload
                return HttpResponse(status=400)

            new_order_line = CustomerOrderLine(
                order=new_order,
                item=tg_item,
                label=tg_item.name,
                quantity=1 if not basket_item['quantity'] else basket_item['quantity'],
                ready=False,
                unit_amount_vat_included=tg_item.price_vat_included,
                unit_amount_vat_excluded=tg_item.price_vat_included / (1 + tg_item.vat_rate),
                unit_vat_amount=(tg_item.price_vat_included / (1 + tg_item.vat_rate)) * tg_item.vat_rate,
                vat_rate=tg_item.vat_rate,
                total_amount_vat_included=float(tg_item.price_vat_included * int(basket_item['quantity'])),
                total_amount_vat_excluded=float((tg_item.price_vat_included / (1 + tg_item.vat_rate)) * int(basket_item['quantity'])),
                total_vat_amount=float(tg_item.vat_rate * int(basket_item['quantity']) * (tg_item.price_vat_included / (1 + tg_item.vat_rate))),
            )
            new_order_line.save()

            # Add Item Customization Option Items
            if len(basket_item['options']) > 0:
                for option in basket_item['options']:
                    try:
                        tg_item = MerchantItem.objects.get(id=option["item"]["id"])
                        tg_item_customization = MerchantItem.objects.get(id=option["id"])
                    except:
                        continue

                    new_order_line_option = CustomerOrderLine(
                        order=new_order,
                        parent_order_line_id=new_order_line.id,
                        item=tg_item,
                        label=tg_item.name,
                        quantity=1 if not option['quantity'] else option['quantity'],
                        ready=False,
                        unit_amount_vat_included=tg_item_customization.price_vat_included,
                        unit_amount_vat_excluded=tg_item_customization.price_vat_included / (1 + tg_item_customization.vat_rate),
                        unit_vat_amount=(tg_item_customization.price_vat_included / (1 + tg_item_customization.vat_rate)) * tg_item_customization.vat_rate,
                        vat_rate=tg_item_customization.vat_rate,
                        total_amount_vat_included=float(tg_item_customization.price_vat_included * int(option['quantity'])),
                        total_amount_vat_excluded=float((tg_item_customization.price_vat_included / (1 + tg_item_customization.vat_rate)) * int(option['quantity'])),
                        total_vat_amount=float(tg_item_customization.vat_rate * int(option['quantity']) * (tg_item_customization.price_vat_included / (1 + tg_item_customization.vat_rate))),
                    )
                    new_order_line_option.save()

        # Retrieve checkout session id
        checkout_session_id = get_stripe_session_id(
            merchant_table_id=merchant_table.id,
            order=new_order,
            customer=customer,
        )

        # Save new checkout session id to this order
        new_order.st_checkout_session_id = checkout_session_id
        new_order.save()

        data = {
            "checkout_session_id": checkout_session_id,
        }
        response = JsonResponse(data)
        return HttpResponse(response, status=200)

    except:
        # Invalid payload
        return HttpResponse(status=400)
