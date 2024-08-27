from flask import jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.app_user import AppUsers, user_schema, users_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


def user_add(request):
    post_data = request.form if request.form else request.json

    new_user = AppUsers.new_user_obj()
    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf8')

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user added", "results": user_schema.dump(new_user)}), 201


@authenticate_return_auth
def user_get_by_id(request, user_id, auth_info):
    users_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if auth_info.user.role == 'super-admin':
        return jsonify({"message": "users found", "results": user_schema.dump(users_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def users_get_all(request, auth_info):
    users_query = db.session.query(AppUsers).all()

    if auth_info.user.role == 'super-admin':
        return jsonify({"message": "users found", "results": users_schema.dump(users_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401
