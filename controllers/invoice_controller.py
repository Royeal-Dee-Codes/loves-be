from flask import jsonify

from db import db
from models.invoice import Invoice, invoice_schema, invoices_schema
from models.app_user import AppUsers, user_schema, users_schema
from models.appointment import Appointment, appt_schema
from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


def invoice_add(request):
    post_data = request.form if request.form else request.json

    new_invoice = Invoice.new_invoice_obj()

    populate_object(new_invoice, post_data)

    db.session.add(new_invoice)
    db.session.commit()

    return jsonify({"message": "invoice added", "results": invoice_schema.dump(new_invoice)}), 201


@authenticate_return_auth
def invoice_get_by_id(request, invoice_id, auth_info):
    invoice_query = db.session.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()

    user_id = db.session.query(AppUsers).filter(Invoice.invoice_id == invoice_id).first()

    if user_id or auth_info.user.role == 'super-admin':
        return jsonify({"message": "invoice found", "results": invoice_schema.dump(invoice_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def invoices_get_all(request, auth_info):
    invoice_query = db.session.query(Invoice).all()

    if auth_info.user.role == 'super-admin':
        return jsonify({"message": "invoices found", "results": invoices_schema.dump(invoice_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def invoice_delete(request, invoice_id, auth_info):
    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "forbidden"}), 403

    if not validate_uuid4(invoice_id):
        return jsonify({"message": "invalid invoice id"}), 400

    invoice_to_delete = db.session.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if not invoice_to_delete:
        return jsonify({"message": "invoice not found"}), 404

    db.session.delete(invoice_to_delete)
    db.session.commit()

    return jsonify({"message": "invoice deleted"}), 200


@authenticate_return_auth
def invoice_update(request, invoice_id, auth_info):
    post_data = request.json()

    if not validate_uuid4(invoice_id):
        return jsonify({"message": "invalid invoice id"}), 400

    invoice_query = db.session.query(Invoice).filter(Invoice.invoice_id == invoice_id)

    if auth_info.user.role != "super-admin":
        invoice_query = invoice_query.filter(Invoice.invoice_id == auth_info.user_id)

    invoice_record = invoice_query.first()

    if invoice_record:
        populate_object(invoice_record, post_data)

        db.session.commit()
        return jsonify({"message": "invoice updated", "results": invoices_schema.dump(invoice_record)}), 200

    return jsonify({"message": "invoice not found"}), 404
