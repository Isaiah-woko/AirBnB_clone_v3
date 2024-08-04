#!/usr/bin/python3
""" a new view for City objects
    that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def retrieve_all_cities_by_states(state_id):
    """Retrieves the list of all cities by State objects"""
    list_of_cities = []
    state_obj = storage.get("State", state_id)
    if state_id is None:
        abort(404)
    for obj in state_obj.cities:
        list_of_cities.append(obj.to_dict())

    return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_city_id(city_id):
    get_city_obj = storage.get("City", str(city_id))

    if get_city_obj is None:
        abort(404)

    return jsonify(get_city_obj.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    get_city_obj = storage.get("City", str(city_id))

    if get_city_obj is None:
        abort(404)

    storage.delete(get_city_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_state(state_id):
    """Creates a city"""
    json_for_city = request.get_json(silent=True)
    if json_for_city is None:
        abort(400, 'Not a JSON')
    if "name" not in json_for_city:
        abort(400, 'Missing name')

    new_city = City(**json_for_city)
    new_city.state_id = state_id
    new_city.save()
    response = jsonify(new_city.to_dict())
    response.status_code = 201

    return response


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_state(city_id):
    """Updates a city_id object"""
    json_for_city = request.get_json(silent=True)
    if json_for_city is None:
        abort(400, 'Not a JSON')
    get_city_obj = storage.get("City", str(city_id))

    if get_city_obj is None:
        abort(404)
    for key, value in json_for_city.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(get_city_obj, key, value)
        get_city_obj.save()
        return jsonify(get_city_obj.to_dict()), 200
