# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.views.generic import RedirectView

from customer.views import CustomerViewSet
from customer_charge.views import CustomerChargeViewSet
from customer_credit_card.views import CustomerCardViewSet
from customer_invoice.views import CustomerInvoiceViewSet
from customer_loyalty_card.views import CustomerLoyaltyCardViewSet, CustomerLoyaltyCardHistoryViewSet
from customer_notification.views import CustomerNotificationViewSet
from customer_order.views import CustomerOrderViewSet
from customer_order_line.views import CustomerOrderLineViewSet
from merchant.views import MerchantViewSet
from merchant_bank_account.views import MerchantBankAccountViewSet
from merchant_charge.views import MerchantChargeViewSet
from merchant_invoice.views import MerchantInvoiceViewSet
from merchant_item.views import MerchantItemViewSet
from merchant_item_category.views import MerchantItemCategoryViewSet
from merchant_item_customization.views import MerchantItemCustomizationViewSet
from merchant_item_customization_option.views import MerchantItemCustomizationOptionViewSet
# from merchant_item_sub_category.views import MerchantItemSubCategoryViewSet
from merchant_loyalty_program.views import MerchantLoyaltyProgramViewSet
from merchant_notification.views import MerchantNotificationViewSet
from merchant_table.views import MerchantTableViewSet
from merchant_upselling.views import MerchantUpsellingViewSet
from user.views import UserViewSet

schema_view = get_swagger_view(title='Ordr API')

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
# router.register(r'customer-charges', CustomerChargeViewSet)
# router.register(r'customer-credit-cards', CustomerCardViewSet)
router.register(r'customer-invoices', CustomerInvoiceViewSet)
# router.register(r'customer-loyalty-cards', CustomerLoyaltyCardViewSet)
# router.register(r'customer-loyalty-card-histories', CustomerLoyaltyCardHistoryViewSet)
# router.register(r'customer-notifications', CustomerNotificationViewSet)
router.register(r'customer-orders', CustomerOrderViewSet)
router.register(r'customer-order-lines', CustomerOrderLineViewSet)
router.register(r'merchants', MerchantViewSet)
# router.register(r'merchant-bank-accounts', MerchantBankAccountViewSet)
# router.register(r'merchant-charges', MerchantChargeViewSet)
router.register(r'merchant-invoices', MerchantInvoiceViewSet)
router.register(r'merchant-items', MerchantItemViewSet)
router.register(r'merchant-item-categories', MerchantItemCategoryViewSet)
router.register(r'merchant-item-customizations', MerchantItemCustomizationViewSet)
router.register(r'merchant-item-customization-options', MerchantItemCustomizationOptionViewSet)
# router.register(r'merchant-item-sub-categories', MerchantItemSubCategoryViewSet)
# router.register(r'merchant-loyalty-programs', MerchantLoyaltyProgramViewSet)
# router.register(r'merchant-notifications', MerchantNotificationViewSet)
router.register(r'merchant-tables', MerchantTableViewSet)
router.register(r'merchant-upsellings', MerchantUpsellingViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/swagger/', schema_view),
    path('api/docs/', include_docs_urls(title='Ordr API')),
    path('create-invoices/', include('utils.urls')),
    path('api/endpoints/', include('utils.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='static/merchant/img/favicon.ico')),
    path('shop/', include('frontend_customer.urls')),
    path('dashboard/', include('frontend_merchant.urls')),
]
