#!/usr/bin/python3

""" objects that handles all default RestFul API actions for Place """
from flask import Blueprint
from models.place_amenity import Place

places_routes = Blueprint('places_routes', __name__)


@places_routes.route('/places', methods=["GET"])
def places_get():
    """returns all Places"""
    return Place.all_places()


@places_routes.route('/places/<place_id>', methods=["GET"])
def places_specific_get(place_id):
    """returns a specific Places"""
    return Place.get_specific_place(place_id)


@places_routes.route('/places', methods=["POST"])
def places_post():
    """adds a new Place and returns it"""
    return Place.create_new_place()


@places_routes.route('/places/<place_id>', methods=["PUT"])
def places_put(place_id):
    """updates a specific Place and returns it"""
    return Place.update_place(place_id)


@places_routes.route('/places/<place_id>', methods=["DELETE"])
def places_delete(place_id):
    """updates a specific Place and returns it"""
    return Place.delete_place(place_id)
