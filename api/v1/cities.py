#!/usr/bin/python3

""" objects that handles all default RestFul API actions for City """
from flask import Blueprint
from models.city import City

cities_routes = Blueprint('cities_routes', __name__)


@cities_routes.route('/cities', methods=["GET"])
def cities_get():
    """ get data for all cities """
    return City.all_cities()

# if country_id is not added, can it be added when new city is added


@cities_routes.route('/cities', methods=["POST"])
def cities_post():
    """ posts data for new city then returns the city data"""
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    return City.create_new_city()


@cities_routes.route('/cities/<city_id>', methods=["GET"])
def cities_specific_get(city_id):
    """ returns specific city data """
    return City.get_specific_city(city_id)


@cities_routes.route('/cities/<city_id>', methods=["PUT"])
def cities_put(city_id):
    """ updates existing city data using specified id """
    return City.update_city(city_id)


@ cities_routes.route('/cities/<city_id>', methods=["DELETE"])
def delete_city(city_id):
    """delete a city"""
    return City.delete_city(city_id)


@cities_routes.route('/cities/<city_id>/country', methods=["GET"])
def cities_specific_country_get(city_id):
    """ Retrieves the data for the country the city belongs to """

    # Using model relationship to get data
    from data import storage
    data = []
    city_data = storage.get('City', 'id', city_id)
    c = city_data[0].country
    data.append({
        "id": c.id,
        "name": c.name,
        "code": c.code,
        "created_at": c.created_at.strftime(City.datetime_format),
        "updated_at": c.updated_at.strftime(City.datetime_format)
    })
    return data
