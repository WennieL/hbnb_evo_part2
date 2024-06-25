#!/usr/bin/python

from datetime import datetime
import uuid
from flask import jsonify, request, abort
from data import storage, USE_DB_STORAGE
from models.place_amenity import Place

datetime_format = "%Y-%m-%dT%H:%M:%S.%f"


@staticmethod
def all_places():
    """ Return all placees """
    pass


@staticmethod
def create_new_place():
    """ Create new place """
    pass


@staticmethod
def get_specific_place(place_id):
    """ get specific palce by place id """
    pass


@staticmethod
def update_place(place_id):
    """ update specific place by place id """
    pass
