""" objects that handles all default RestFul API actions for Place """
from api.v1 import api_routes
from models.place_amenity import Place
from services import place_service


@api_routes.route('/places', methods=["POST"])
def places_post():
    """adds a new Place and returns it"""
    return place_service.create_new_place()


@api_routes.route('/places', methods=["GET"])
def places_get():
    """returns all Places"""
    return place_service.all_places()


@api_routes.route('/places/<place_id>', methods=["GET"])
def places_specific_get(place_id):
    """returns a specific Places"""
    return place_service.get_specific_place(place_id)


@api_routes.route('/places/<place_id>', methods=["PUT"])
def places_put(place_id):
    """updates a specific Place and returns it"""
    return place_service.update_place(place_id)
