from flask import Blueprint, request

import controllers

service = Blueprint('services', __name__)


@service.route('/service', methods=['POST'])
def service_add():
    return controllers.service_add(request)


@service.route('/service/<service_id>', methods=['GET'])
def service_get_by_id(service_id):
    return controllers.service_get_by_id(request, service_id)


@service.route('/services', methods=['GET'])
def services_get_all():
    return controllers.services_get_all(request)
