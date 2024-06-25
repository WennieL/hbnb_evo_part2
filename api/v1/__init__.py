# __init__.py in api/v1
#!/usr/bin/python3


""" Blueprint for API """
from flask import Blueprint

from api.v1.amenities import *
from api.v1.cities import *
from api.v1.countries import *
from api.v1.places import *
from api.v1.reviews import *
from api.v1.users import *

api_routes = Blueprint('api_routes', __name__, url_prefix='/api/v1')
