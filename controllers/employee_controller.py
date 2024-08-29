from flask import jsonify
from flask_bcrypt import generate_password_hash, check_password_hash

from db import db
from models.app_user import AppUsers, user_schema, users_schema
from models.auth_tokens import AuthTokens, auth_token_schema
from models.employees import Employees, employee_schema, employees_schema
from util.validate_uuid4 import validate_uuid4
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


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

    if auth_info.user != None:
        if auth_info.user.role == 'super-admin':
            return jsonify({"message": "employee found", "results": employee_schema.dump(employee_query)}), 200

    elif auth_info.employee != None:
        if auth_info.employee.role == 'employee':
            return jsonify({"message": "employee found", "results": employees_schema.dump(employee_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def employees_get_all(request, auth_info):
    employee_query = db.session.query(Employees).all()

    if auth_info.user != None:
        if auth_info.user.role == 'super-admin':
            return jsonify({"message": "employees found", "results": employees_schema.dump(employee_query)}), 200

    elif auth_info.employee != None:
        if auth_info.employee.role == 'employee':
            return jsonify({"message": "employees found", "results": employees_schema.dump(employee_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def employee_delete(request, employee_id, auth_info):
    if validate_uuid4(employee_id) == False:
        return jsonify({"message": "invalid employee id"}), 404

    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == auth_info.user.user_id).first()

    if user_query != None:
        if user_query.role == 'super-admin':
            employee = db.session.query(Employees).filter(Employees.employee_id == employee_id).first()

            db.session.delete(employee)
            db.session.commit()

            return jsonify({"message": "employee deleted"}), 200

    return jsonify({"message": "unauthorized"}), 403


@authenticate_return_auth
def employee_update(request, employee_id, auth_info):
    post_data = request.get_json()
    new_password = post_data.get("password")
    current_password = post_data.get("current_password")
    validate_employee_id = validate_uuid4(employee_id)

    if validate_employee_id:
        if auth_info.user.role == 'super-admin':
            employee_query = db.session.query(Employees).filter(Employees.employee_id == employee_id).first()

        else:
            employee_query = db.session.query(Employees).filter(Employees.employee_id == auth_info.employee.employee_id).first()

    else:
        return jsonify({"message": "invalid employee id"}), 400

    if employee_query:
        if new_password:
            if not check_password_hash(employee_query.password, current_password):
                return jsonify({"message": "incorrenct current password"}), 400

            post_data["password"] = generate_password_hash(post_data["password"]).decode('utf8')

            del post_data["current_password"]

        populate_object(employee_query, post_data)
        db.session.commit()

        return jsonify({"message": "employee updated", "results": employee_schema.dump(employee_query)}), 200

    else:
        return jsonify({"message": "invalid employee id"}), 400
