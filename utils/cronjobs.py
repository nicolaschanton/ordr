# -*- coding: utf-8 -*-

from .stripe_utils import create_merchant, create_bank_account
from merchant.models import Merchant
from merchant_bank_account.models import MerchantBankAccount


def save_merchant_bank_account():
    for merchant_bank_account in MerchantBankAccount.objects.filter(
        stripe_bank_account_id__isnull=True,
        bank_iban__isnull=False,
        account_holder_name__isnull=False,
    ):
        if merchant_bank_account.merchant.stripe_customer_id:
            create_bank_account(
                merchant_bank_account=merchant_bank_account,
                verify_amount=300,
            )
        else:
            create_merchant(
                merchant=merchant_bank_account.merchant
            )
            create_bank_account(
                merchant_bank_account=merchant_bank_account,
                verify_amount=300,
            )
    return


def update_credit_cards_status():

    return


def update_customer_loyalty_cards():

    return


def charge_merchant_invoice():

    return
