# coding: utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.template import loader
from django.conf import settings
import json
from datetime import datetime, timedelta
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

import pdfkit
from django.core.files import File
import os

from customer_order.models import CustomerOrder
from customer_order_line.models import CustomerOrderLine
from customer_invoice.models import CustomerInvoice
from .customer_order_utils import update_order_financial


def create_customer_invoice_pdf(request, sharable_order_id, sharable_invoice_id):
    try:
        order = CustomerOrder.objects.filter(id=sharable_order_id).first()
        customer_invoice = CustomerInvoice.objects.filter(id=sharable_invoice_id).first()
        order_lines = CustomerOrderLine.objects.filter(order=order)

        if order and order_lines:

            if customer_invoice:

                # Update Financial Values
                update_order_financial(order=order)

                context = {
                    "order": order,
                    "order_lines": order_lines,
                    "customer_invoice": customer_invoice
                }
                template = loader.get_template('invoices/customer_invoice_template.html')

                ## HTML to PDF conversion
                #html = template.render(context)
                #filename = str(str(customer_invoice.id) + "-" + str(datetime.now()) + "-" + customer_invoice.order.customer.full_name() + "-" + customer_invoice.invoice_number_text + '.pdf')
                #pdfkit.from_string(html, filename)
                #pdf = open(filename)
                #pdf.close()
#
                ## Updating Customer Invoice object
                #if customer_invoice.invoice_file:
                #    customer_invoice.delete_invoice_file()
                #    customer_invoice.save()
                #    customer_invoice.invoice_file.save(filename, content=File(open(filename, 'rb')))
                #else:
                #    customer_invoice.invoice_file.save(filename, content=File(open(filename, 'rb')))
#
                ## Cleaning the temporary file
                #os.remove(filename)

                response = HttpResponse(template.render(context, request))

                return response

            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    except:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

