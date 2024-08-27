from flask import Blueprint, request

import controllers

users = Blueprint('users', __name__)


@users.route('/user', methods=['POST'])
def add_user():
    return controllers.user_add(request)


@users.route('/user/<user_id>', methods=['GET'])
def user_get_by_id(user_id):
    return controllers.user_get_by_id(request, user_id)


@users.route('/users', methods=['GET'])
def get_all_users():
    return controllers.users_get_all(request)
