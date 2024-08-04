#!/usr/bin/python3
"""
A new view for Place objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """get all"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """get"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, 'Not a JSON')
    if "user_id" not in json_data:
        abort(400, 'Missing user_id')
    if "name" not in json_data:
        abort(400, 'Missing name')

    user = storage.get("User", json_data["user_id"])
    if user is None:
        abort(404)

    json_data["city_id"] = city_id
    new_place = Place(**json_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, 'Not a JSON')

    for key, value in json_data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
