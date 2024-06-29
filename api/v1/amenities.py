#!/usr/bin/python3

""" objects that handles all default RestFul API actions for Amenity """

from flask import Blueprint
from models.place_amenity import Amenity

amenities_routes = Blueprint('amenities_routes', __name__)


@amenities_routes.route('/amenities', methods=["POST"])
def amenity_post():
    """ Creates a new Amenity and returns it """
    return Amenity.create_new_amenity()


@amenities_routes.route('/amenities', methods=["GET"])
def amenity_get():
    """ Gets all Amenities """
    return Amenity.all_amenity()


@amenities_routes.route('/amenities/<amenity_id>', methods=["GET"])
def amenity_specific_get(amenity_id):
    """ Gets a specific Amenity """
    return Amenity.get_specific_amenity(amenity_id)


@amenities_routes.route('/amenities/<amenity_id>', methods=["PUT"])
def amenity_put(amenity_id):
    """ Updates a specific Amenity and returns it """
    return Amenity.update_amenity(amenity_id)


@amenities_routes.route('/amenities/<amenity_id>', methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes an existing amenity by amenity_id"""
    return Amenity.delete_amenity(amenity_id)
