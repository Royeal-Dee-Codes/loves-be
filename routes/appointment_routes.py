from flask import Blueprint, request

import controllers

appointment = Blueprint('appointment', __name__)


@appointment.route('/appointment', methods=['POST'])
def appt_add():
    return controllers.appt_add(request)


@appointment.route('/appointment/<appt_id>', methods=['GET'])
def appt_get_by_id(appt_id):
    return controllers.appt_get_by_id(request, appt_id)


@appointment.route('/appointments', methods=['GET'])
def appts_get_all():
    return controllers.appt_get_all(request)


@appointment.route('/appointment/delete/<appt_id>', methods=['DELETE'])
def appt_delete(appt_id):
    return controllers.appt_delete(request, appt_id)


@appointment.route('/appointment/<appt_id>', methods=['PUT'])
def appt_update(appt_id):
    return controllers.appt_update(request, appt_id)
