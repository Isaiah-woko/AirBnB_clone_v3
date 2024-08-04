#!/usr/bin/python3
"""
A new view for Review objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """get by place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """get"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    
    json_for_review = request.get_json(silent=True)
    if json_for_review is None:
        abort(400, 'Not a JSON')
    
    if "user_id" not in json_for_review:
        abort(400, 'Missing user_id')
    user = storage.get("User", json_for_review["user_id"])
    if user is None:
        abort(404)
    
    if "text" not in json_for_review:
        abort(400, 'Missing text')

    new_review = Review(**json_for_review)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    json_for_review = request.get_json(silent=True)
    if json_for_review is None:
        abort(400, 'Not a JSON')

    for key, value in json_for_review.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
