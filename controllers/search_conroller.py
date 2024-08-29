from flask import jsonify
from sqlalchemy import func

from db import db
from models.app_user import AppUsers, users_schema, user_schema
from models.employees import Employees, employees_schema, employee_schema
from models.invoice import Invoice, invoices_schema, invoice_schema
from models.service import Service, services_schema, service_schema
from models.appointment import Appointment, appts_schema, appt_schema
from lib.authenticate import authenticate


@authenticate
def users_get_by_search(request):
    search_term = request.args.get('q').lower()

    user_data = db.session.query(AppUsers).filter(db.or_(db.func.lower(AppUsers.first_name).contains(search_term), db.func.lower(AppUsers.last_name).contains(search_term), db.func.lower(AppUsers.email).contains(search_term))).order_by(AppUsers.last_name.asc())

    return jsonify({"message": "users found", "results": users_schema.dump(user_data)}), 200


@authenticate
def employees_get_by_search(request):
    search_term = request.args.get('q').lower()

    employee_data = db.session.query(Employees).filter(db.or_(db.func.lower(Employees.first_name)container(search_term), db.func.lower(Employees.last_name).contains(search_term), db.func.lower(Employees.email).contains(search_term))).order_by(Employees.last_name.asc())

    return jsonify({"message": "employees found", "results": employees_schema.dump(employee_data)}), 200
