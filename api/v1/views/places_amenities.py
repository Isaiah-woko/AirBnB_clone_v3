#!/usr/bin/python3
"""
route for handling place and amenities linking
"""
from flask import jsonify, abort
from os import getenv
from models import storage
from api.v1.views import app_views


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def retrieve_amenity(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    get_obj = storage.get("Place", str(place_id))

    all_amenities = []

    if get_obj is None:
        abort(404)

    for obj in get_obj.amenities:
        all_amenities.append(obj.to_dict())

    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    """
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)

    get_obj = storage.get("Place", place_id)
    found = 0

    for obj in get_obj.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                get_obj.amenities.remove(obj)
            else:
                get_obj.amenity_ids.remove(obj.id)
            get_obj.save()
            found = 1
            break

    if found == 0:
        abort(404)
    else:
        response = jsonify({})
        response.status_code = 200
        return response


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place
    """

    get_obj = storage.get("Place", str(place_id))
    amenity_obj = storage.get("Amenity", str(amenity_id))
    found_amenity = None

    if not get_obj or not amenity_obj:
        abort(404)

    for obj in get_obj.amenities:
        if str(obj.id) == amenity_id:
            found_amenity = obj
            break

    if found_amenity is not None:
        return jsonify(found_amenity.to_dict())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        get_obj.amenities.append(amenity_obj)
    else:
        get_obj.amenity_ids.append(amenity_obj.id)

    get_obj.save()

    resp = jsonify(amenity_obj.to_dict())
    resp.status_code = 201

    return resp
