# cities.py
#!/usr/bin/python3

""" objects that handles all default RestFul API actions for City """
from flask import jsonify, request, abort
from api.v1 import api_routes
from models.city import City
from services import city_service


@api_routes.route('/cities', methods=["GET"])
def cities_get():
    """ get data for all cities """
    return city_service.all_cities()


@api_routes.route('/cities', methods=["POST"])
def cities_post():
    """ posts data for new city then returns the city data"""
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    return city_service.create_new_city()


@api_routes.route('/cities/<city_id>', methods=["GET"])
def cities_specific_get(city_id):
    """ returns specific city data """
    return city_service.get_specific_city(city_id)


@api_routes.route('/cities/<city_id>', methods=["PUT"])
def cities_put(city_id):
    """ updates existing city data using specified id """
    return city_service.update_city(city_id)


@ api_routes.route('/cities/<city_id>', methods=["DELETE"])
def delete_city(city_id):
    """delete a city"""
    return city_service.delete_city(city_id)


@api_routes.route('/cities/<city_id>/country', methods=["GET"])
def cities_specific_country_get(city_id):
    """ Retrieves the data for the country the city belongs to """

    # Using model relationship to get data
    from data import storage
    city_data = storage.get('City', city_id)
    if not city_data:
        abort(404, description=f"City with ID: {city_id} not found")

    c = city_data.country
    data = {
        "id": c.id,
        "name": c.name,
        "code": c.code,
        "created_at": c.created_at.strftime(city_service.datetime_format),
        "updated_at": c.updated_at.strftime(city_service.datetime_format)
    }
    return jsonify(data), 200
