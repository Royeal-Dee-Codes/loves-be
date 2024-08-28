from flask import jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.employees import Employees, employee_schema, employees_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth


def employee_add(request):
    post_data = request.form if request.form else request.json

    new_employee = Employees.new_emp_obj()

    populate_object(new_employee, post_data)

    new_employee.password = generate_password_hash(new_employee.password).decode('utf8')

    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"message": "employee added", "results": employee_schema.dump(new_employee)}), 201


@authenticate_return_auth
def employee_get_by_id(request, employee_id, auth_info):
    employee_query = db.session.query(Employees).filter(Employees.employee_id == employee_id).first()

    if employee_id == str(auth_info.employee.employee_id) or auth_info.employee.role == 'employee':
        return jsonify({"message": "employee found", "results": employee_schema.dump(employee_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def employees_get_all(request, auth_info):
    employee_query = db.session.query(Employees).all()
    print(auth_info.user)
    if auth_info.employee != None:
        if auth_info.employee.role == 'employee':
            return jsonify({"message": "employees found", "results": employees_schema.dump(employee_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401
