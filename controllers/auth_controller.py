from flask import jsonify
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta

from db import db
from models.auth_tokens import AuthTokens, auth_token_schema
from models.app_user import AppUsers
from models.employees import Employees


def auth_token_add(request):
    post_data = request.form if request.form else request.json
    email = post_data.get('email')
    password = post_data.get('password')

    if not email or not password:
        return jsonify({"message": "invalid login"}), 401

    now_datetime = datetime.now()
    expiration_datetime = now_datetime + timedelta(hours=12)

    user_query = db.session.query(AppUsers).filter(AppUsers.email == email).first()
    employee_query = db.session.query(Employees).filter(Employees.email == email).first()

    if user_query:
        is_password_valid = check_password_hash(user_query.password, password)

        if is_password_valid == False:
            return jsonify({"message": "invalid password"}), 401

        existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_query.user_id).all()

        if existing_tokens:
            for token in existing_tokens:
                if token.expiration < now_datetime:
                    db.session.delete(token)

        elif employee_query:
            is_password_valid = check_password_hash(employee_query.password, password)

            if is_password_valid == False:
                return jsonify({"message": "invalid password"}), 401

            existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.employee_id == employee_query.employee_id).all()

            if existing_tokens:
                for token in existing_tokens:
                    if token.expiration < now_datetime:
                        db.session.delete(token)

        new_token = AuthTokens(expiration_datetime, user_query.user_id)

        db.session.add(new_token)
        db.session.commit()

        if new_token:
            return jsonify({"message": "authorization successful", "result": auth_token_schema.dump(new_token)}), 201

    else:
        return jsonify({"message": "ERROR: Request must be made in JSON format"}), 400
