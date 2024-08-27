from flask import Blueprint, request

import controllers

invoice = Blueprint('invoice', __name__)


@invoice.route('/invoice', methods=['POST'])
def invoice_add():
    return controllers.invoice_add(request)


@invoice.route('/invoice/<invoice_id>', methods=['GET'])
def invoice_get_by_id(invoice_id):
    return controllers.invoice_get_by_id(request, invoice_id)


@invoice.route('/invoices', methods=['GET'])
def invoices_get_all():
    return controllers.invoices_get_all(request)
