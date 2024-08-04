#!/usr/bin/python3
"""
A new view for City objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def retrieve_all_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)

    list_of_cities = [city.to_dict() for city in state_obj.cities]
    return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_city(city_id):
    """Retrieves a City object"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)

    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)

    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)

    json_for_city = request.get_json(silent=True)
    if json_for_city is None:
        abort(400, 'Not a JSON')
    if "name" not in json_for_city:
        abort(400, 'Missing name')

    new_city = City(**json_for_city)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)

    json_for_city = request.get_json(silent=True)
    if json_for_city is None:
        abort(400, 'Not a JSON')

    for key, value in json_for_city.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
