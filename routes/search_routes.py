from flask import request, Blueprint

import controllers

search = Blueprint('search', __name__)


@search.route('/users/search', methods=['GET'])
def users_get_by_search():
    return controllers.users_get_by_search(request)


@search.route('/employees/search', methods=['GET'])
def employees_get_by_search():
    return controllers.employees_get_by_search(request)


@search.route('/invoices/search', methods=['GET'])
def invoices_get_by_search():
    return controllers.invoices_get_by_search(request)


@search.route('/services/search', methods=['GET'])
def services_get_by_search():
    return controllers.services_get_by_search(request)


@search.route('/appointments/search', methods=['GET'])
def appointments_get_by_search():
    return controllers.appointments_get_by_search(request)
