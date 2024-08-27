from flask import Blueprint, request

import controllers

employees = Blueprint('employees', __name__)


@employees.route('/employee', methods=['POST'])
def employee_add():
    return controllers.employee_add(request)


@employees.route('/employee/<employee_id>', methods=['GET'])
def employee_get_by_id(employee_id):
    return controllers.employee_get_by_id(request, employee_id)


@employees.route('/employees', methods=['GET'])
def employees_get_all():
    return controllers.employees_get_all(request)
