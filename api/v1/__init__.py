#!/usr/bin/python3

from flask import Blueprint

# import API
from .users import users_routes
from .reviews import reviews_routes
from .places import places_routes
from .countries import countries_routes
from .cities import cities_routes
from .amenities import amenities_routes


# Create the main Blueprint
api_routes = Blueprint('api_routes', __name__, url_prefix='/api/v1')


api_routes.register_blueprint(users_routes)
api_routes.register_blueprint(reviews_routes)
api_routes.register_blueprint(places_routes)
api_routes.register_blueprint(countries_routes)
api_routes.register_blueprint(cities_routes)
api_routes.register_blueprint(amenities_routes)
