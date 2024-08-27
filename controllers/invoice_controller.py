from flask import jsonify

from db import db
from models.invoice import Invoice, invoice_schema, invoices_schema
from models.appointment import Appointment, appt_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


def invoice_add(request):
    post_data = request.form if request.form else request.json

    new_invoice = Invoice.new_invoice_obj()

    populate_object(new_invoice, post_data)

    db.session.add(new_invoice)
    db.session.commit()

    return jsonify({"message": "invoice needed", "results": invoice_schema.dump(new_invoice)}), 201


@authenticate_return_auth
def invoice_get_by_id(request, user_id, invoice_id, auth_info):
    invoice_query = db.session.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()

    if user_id == str(auth_info.user.user_id) or auth_info.user.role == 'super-admin':
        return jsonify({"message": "invoice found", "result": invoice_schema.dump(invoice_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401


authenticate_return_auth


def invoice_get_all(request, auth_info):
    invoice_query = db.session.query(Invoice).all()

    if auth_info.user.role == 'super-admin':
        return jsonify({"message": "invoices found", "results": invoices_schema.dump(invoice_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401
