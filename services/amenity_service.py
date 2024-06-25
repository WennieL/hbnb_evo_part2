#!/usr/bin/python

from datetime import datetime
import uuid
from flask import jsonify, request, abort
from data import storage, USE_DB_STORAGE
from models.place_amenity import Amenity

datetime_format = "%Y-%m-%dT%H:%M:%S.%f"


@staticmethod
def all_amenity():
    """ Return all amenities """
    pass


@staticmethod
def create_new_amenity():
    """ Create new amenoty """
    pass


@staticmethod
def get_specific_amenity(amenity_id):
    """ get specific amenity by amenity id """
    pass


@staticmethod
def update_amenity(amenity_id):
    """ update specific city by city id """
    pass
