from flask import Blueprint, request

import controllers

appointment = Blueprint('appointment', __name__)


@appointment.route('/appointment', methods=['POST'])
def appointment_add():
    return controllers.appt_add(request)


@appointment.route('/appointment/<appt_id>', methods=['GET'])
def appointment_get_by_id(appt_id):
    return controllers.appt_get_by_id(request, appt_id)


@appointment.route('/appointments', methods=['GET'])
def appointments_get_all():
    return controllers.appt_get_all(request)
