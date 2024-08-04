#!/usr/bin/python3
""" a new view for State objects
    that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_all_state():
    """Retrieves the list of all State objects"""
    list_of_state = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        list_of_state.append(obj.to_dict())

    return jsonify(list_of_state)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_state_id(state_id):
    get_state_obj = storage.get("State", str(state_id))

    if get_state_obj is None:
        abort(404)

    return jsonify(get_state_obj.to_dict())


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    get_state_obj = storage.get("State", str(state_id))

    if get_state_obj is None:
        abort(404)

    storage.delete(get_state_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    json_for_state = request.get_json(silent=True)
    if json_for_state is None:
        abort(400, 'Not a JSON')
    if "name" not in json_for_state:
        abort(400, 'Missing name')

    new_state = State(**json_for_state)
    new_state.save
    response = jsonify(new_state.to_dict())
    response.status_code = 201

    return response


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    json_for_state = request.get_json(silent=True)
    if json_for_state is None:
        abort(400, 'Not a JSON')
    get_state_obj = storage.get("State", str(state_id))

    if get_state_obj is None:
        abort(404)
    for key, value in json_for_state.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(get_state_obj, key, value)
        get_state_obj.save()
        return jsonify(get_state_obj.to_dict()), 200

