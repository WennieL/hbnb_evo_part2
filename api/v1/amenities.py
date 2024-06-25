""" objects that handles all default RestFul API actions for Amenity """
from api.v1 import api_routes
from models.place_amenity import Amenity
from services import amenity_service


@api_routes.route('/amenities', methods=["POST"])
def amenity_post():
    """ Creates a new Amenity and returns it """
    return amenity_service.create_new_amenity()


@api_routes.route('/amenities', methods=["GET"])
def amenity_get():
    """ Gets all Amenities """
    return amenity_service.all_amenity()


@api_routes.route('/amenities/<amenity_id>', methods=["GET"])
def amenity_specific_get(amenity_id):
    """ Gets a specific Amenity """
    return amenity_service.get_specific_amenity(amenity_id)


@api_routes.route('/amenities/<amenity_id>', methods=["PUT"])
def amenity_put(amenity_id):
    """ Updates a specific Amenity and returns it """
    return amenity_service.update_amenity(amenity_id)
