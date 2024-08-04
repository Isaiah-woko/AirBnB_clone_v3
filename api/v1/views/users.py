#!/usr/bin/python3
"""
A new view for User objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves"""
    users = storage.all("User").values()
    users = [user.to_dict() for user in users]
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves"""
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes"""
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)

    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates"""
    json_for_user = request.get_json(silent=True)
    if json_for_user is None:
        abort(400, 'Not a JSON')
    if "name" not in json_for_user:
        abort(400, 'Missing name')
    if "email" not in json_for_user:
        abort(400, 'Missing email')
    if "password" not in json_for_user:
        abort(400, 'Missing password')

    new_user = User(**json_for_user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update"""
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)

    json_for_user = request.get_json(silent=True)
    if json_for_user is None:
        abort(400, 'Not a JSON')

    for key, value in json_for_user.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
