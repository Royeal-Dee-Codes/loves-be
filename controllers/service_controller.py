from flask import jsonify

from db import db
from models.service import Service, service_schema, services_schema
from models.app_user import AppUsers, user_schema, users_schema
from util.reflection import populate_object
from util.validate_uuid4 import validate_uuid4
from lib.authenticate import authenticate, authenticate_return_auth


def service_add(request):
    post_data = request.form if request.form else request.json
    user_id = post_data.get("user_id")

    new_service = Service.new_service_obj()

    populate_object(new_service, post_data)

    db.session.add(new_service)
    db.session.commit()

    return jsonify({"message": "service added", "results": service_schema.dump(new_service)}), 201


@authenticate_return_auth
def service_get_by_id(request, service_id, auth_info):
    service_query = db.session.query(Service).filter(Service.service_id == service_id).first()

    user_id = db.session.query(AppUsers).filter(Service.service_id == service_id).first()

    if user_id or auth_info.user.role == 'super-admin':
        return jsonify({"message": "service found", "results": service_schema.dump(service_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def services_get_all(request, auth_info):
    service_query = db.session.query(Service).all()

    if auth_info.user.role == 'super-admin':
        return jsonify({"message": "services found", "results": services_schema.dump(service_query)}), 200

    else:
        return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def service_delete(request, service_id, auth_info):
    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "forbidden"}), 403

    if not validate_uuid4(service_id):
        return jsonify({"message": "invalid service id"}), 400

    service_to_delete = db.session.query(Service).filter(Service.service_id == service_id).first()
    if not service_to_delete:
        return jsonify({"message": "service not found"}), 404

    db.session.delete(service_to_delete)
    db.session.commit()

    return jsonify({"message": "service deleted"}), 200
