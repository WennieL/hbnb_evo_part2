#!/usr/bin/python3

""" objects that handles all default RestFul API actions for Country """
from flask import Blueprint
from models.country import Country

countries_routes = Blueprint('countries_routes', __name__)


@countries_routes.route('/countries', methods=["POST"])
def countries_post():
    """ posts data for new country then returns the country data"""
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    return Country.create_country()


@countries_routes.route('/countries', methods=["GET"])
def countries_get():
    """ returns countires data """
    return Country.all_country()


@countries_routes.route('/countries/<country_code>', methods=["GET"])
def countries_specific_get(country_code):
    """ returns specific country data """
    return Country.specific(country_code)


@countries_routes.route('/countries/<country_code>', methods=["PUT"])
def countries_put(country_code):
    """ updates existing country data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    # can only update name
    return Country.update(country_code)


@countries_routes.route('/countries/<country_code>/cities', methods=["GET"])
def countries_specific_cities_get(country_code):
    """ returns cities data of specified country """

    # If you're using DB Storage, you can probably use the model's relationship to save yourself some work
    # Look in the example endpoints in app.py for a hint

    return Country.cities_data(country_code)
