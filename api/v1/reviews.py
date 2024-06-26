#!/usr/bin/python3

""" objects that handles all default RestFul API actions for User"""
from api.v1 import api_routes
from models.review import Review


@api_routes.route('/reviews', methods=["GET"])
def reviews_get():
    """get all reviews"""
    return Review.all_reviews()


@api_routes.route('/places/<place_id>/reviews', methods=['GET'])
def reviews_from_place_id(place_id):
    """returns specified user"""
    # use the User class' static .specific method
    return Review.get_specific_review_by_place_id(place_id)


@api_routes.route('/users/<user_id>/reviews', methods=['GET'])
def reviews_from_user_id(user_id):
    """returns specified user"""
    # use the User class' static .specific method
    return Review.get_specific_review_by_user_id(user_id)


@api_routes.route('/reviews/<review_id>', methods=['GET'])
def reviews_from_review_id(review_id):
    """returns specified user"""
    # use the User class' static .specific method
    return Review.get_specific_review_by_review_id(review_id)


@api_routes.route('/places/<place_id>/reviews', methods=["POST"])
def review_create(place_id):
    """ posts data for new user then returns the user data"""
    # -- Usage example --
    # curl -X POST localhost:5000/api/v1/users /
    #   -H "Content-Type: application/json" /
    #   -d '{"first_name":"Peter","last_name":"Parker","email":"p.parker@daily-bugle.net","password":"123456"}'

    # use the User class' static .create method
    return Review.create_new_review(place_id)


@api_routes.route('/reviews/<place_id>', methods=["PUT"])
def review_update(place_id):
    """ updates existing user data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    # use the User class' static .update method
    # can only update first_name and last_name
    return Review.update_review(place_id)


@api_routes.route('/reviews/<review_id>', methods=["DELETE"])
def review_delete(review_id):
    """ updates existing user data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    # use the User class' static .update method
    # can only update first_name and last_name
    return Review.delete_review(review_id)
