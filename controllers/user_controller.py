from flask import jsonify
from flask_bcrypt import generate_password_hash, check_password_hash

from db import db
from models.app_user import AppUsers, user_schema, users_schema
from util.validate_uuid4 import validate_uuid4
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


@authenticate_return_auth
def user_delete(request, user_id, auth_info):
    if validate_uuid4(user_id) == False:
        return jsonify({"message": "invalid user id"}), 404

    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == auth_info.user.user_id).first()

    if user_query != None:
        if user_query.role == 'super-admin':
            user = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

            db.session.delete(user)
            db.session.commit()

            return jsonify({"message": "user deleted"}), 200

    return jsonify({"message": "unauthorized"}), 403


@authenticate_return_auth
def user_update(request, user_id, auth_info):
    post_data = request.get_json()
    new_password = post_data.get("password")
    current_password = post_data.get("current_password")
    validate_user_id = validate_uuid4(user_id)

    if validate_user_id:
        if auth_info.user.role == 'super-admin':
            user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

        else:
            user_query = db.session.query(AppUsers).filter(AppUsers.user_id == auth_info.user.user_id).first()

    else:
        return jsonify({"message": "invalid user id"}), 400

    if user_query:
        if new_password:
            if not check_password_hash(user_query.password, current_password):
                return jsonify({"message": "incorrenct current password"}), 400

            post_data["password"] = generate_password_hash(post_data["password"]).decode('utf8')

            del post_data["current_password"]

        populate_object(user_query, post_data)
        db.session.commit()

        return jsonify({"message": "user updated", "results": user_schema.dump(user_query)}), 200

    else:
        return jsonify({"message": "invalid user id"}), 400
