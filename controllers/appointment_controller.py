from flask import jsonify

from db import db
from models.app_user import AppUsers, AppUsersSchema
from models.appointment import Appointment, appt_schema, appts_schema
from models.service import Service
from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


def appt_add(request):
    post_data = request.form if request.form else request.json
    service_id = post_data.get("service_id")
    service_query = db.session.query(Service).filter(Service.service_id == service_id).first()

    new_appointment = Appointment.new_appt_obj()

    populate_object(new_appointment, post_data)

    new_appointment.user_id = service_query.user_id

    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({"message": "appointment added", "results": appt_schema.dump(new_appointment)}), 201


@authenticate_return_auth
def appt_get_by_id(request, appt_id, auth_info):
    appt_query = db.session.query(Appointment).filter(Appointment.appt_id == appt_id).first()

    user_id = db.session.query(AppUsers).filter(AppUsers.user_id == auth_info.user.user_id).first()

    if user_id or auth_info.user.role == 'super-admin':
        return jsonify({"message": "appointment found", "results": appt_schema.dump(appt_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def appt_get_all(request, auth_info):
    appt_query = db.session.query(Appointment).all()

    if auth_info.user.role == 'super-admin':
        return jsonify({"message": "appointments found", "results": appts_schema.dump(appt_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def appt_delete(request, appt_id, auth_info):
    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "forbidden"}), 403

    if not validate_uuid4(appt_id):
        return jsonify({"message": "invalid appointment id"}), 400

    appointment_to_delete = db.session.query(Appointment).filter(Appointment.appt_id == appt_id).first()
    if not appointment_to_delete:
        return jsonify({"message": "appointment not found"}), 404

    db.session.delete(appointment_to_delete)
    db.session.commit()

    return jsonify({"message": "appointment deleted"}), 200


@authenticate_return_auth
def appt_update(request, appt_id, auth_info):
    post_data = request.json

    if not validate_uuid4(appt_id):
        return jsonify({"message": "invalid appointment id"}), 400

    appt_query = db.session.query(Appointment).filter(Appointment.appt_id == appt_id)

    if auth_info.user.role != "super-admin":
        appt_query = appt_query.filter(Appointment.appt_id == auth_info.user_id)

    appointment_record = appt_query.first()

    if appointment_record:
        populate_object(appointment_record, post_data)

        db.session.commit()
        return jsonify({"message": "appointment updated", "results": appt_schema.dump(appointment_record)}), 200

    return jsonify({"message": "appointment not found"}), 404
