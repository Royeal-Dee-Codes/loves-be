from flask import jsonify

from db import db
from models.app_user import AppUsers, AppUsersSchema
from models.appointment import Appointment, appt_schema, appts_schema
from models.service import Service, service_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


def appt_add(request):
    post_data = request.form if request.form else request.json
    appt_id = post_data.get("appt_id")

    new_appointment = Appointment.new_appt_obj()

    populate_object(new_appointment, post_data)

    if appt_id:
        appt_query = db.session.query(Appointment).filter(Appointment.appt_id == appt_id).first()

        if appt_query == None:
            return jsonify({"message": "appt id required"}), 400

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
