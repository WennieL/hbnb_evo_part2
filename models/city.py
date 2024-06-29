#!/usr/bin/python
""" City model """

from datetime import datetime
import uuid
import re
from flask import jsonify, request, abort
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data import storage, USE_DB_STORAGE, Base
# from models.country import Country


class City(Base):
    """Representation of city """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"

    # Class attrib defaults
    id = None
    created_at = None
    updated_at = None
    __name = ""
    __country_id = ""

    if USE_DB_STORAGE:
        __tablename__ = 'cities'
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.now())
        updated_at = Column(DateTime, nullable=False, default=datetime.now())
        __name = Column("name", String(128), nullable=False)
        __country_id = Column("country_id", String(
            128), ForeignKey('countries.id'), nullable=False)

        country = relationship("Country", back_populates="cities")
        place = relationship("Place", back_populates="city")

    # constructor
    def __init__(self, *args, **kwargs):
        """ constructor """
        # Set object instance defaults
        self.id = str(uuid.uuid4())

        # Note that db records have a default of datetime.now()
        if not USE_DB_STORAGE:
            self.created_at = datetime.now().timestamp()
            self.updated_at = self.created_at

        # Only allow country_id, name.
        # Note that setattr will call the setters for these 2 attribs
        if kwargs:
            for key, value in kwargs.items():
                if key in ["country_id", "name"]:
                    setattr(self, key, value)

    @property
    def name(self):
        """Getter for private prop name"""
        return self.__name

    @name.setter
    def name(self, value):
        """Setter for private prop name"""

        # ensure that the value is not spaces-only and is alphabets + spaces only
        is_valid_name = len(value.strip()) > 0 and re.search(
            "^[a-zA-Z ]+$", value)
        if is_valid_name:
            self.__name = value
        else:
            raise ValueError("Invalid city name specified: {}".format(value))

    @property
    def country_id(self):
        """Getter for private prop country_id"""
        return self.__country_id

    @country_id.setter
    def country_id(self, value):
        """Setter for private prop country_id"""
        # ensure that the specified country id actually exists before setting
        if storage.get('Country', value) is not None:
            self.__country_id = value
        else:
            raise ValueError("Invalid country_id specified: {}".format(value))

    # --- Static methods ---

    @staticmethod
    def all_cities():
        """ Return all reviews """
        data = []

        try:
            city_data = storage.get('City')
        except IndexError as exc:
            print("Error: ", exc)
            abort(500, "Unable to load cities!")

        if USE_DB_STORAGE:
            for row in city_data:
                data.append({
                    "id": row.id,
                    "country_id": row.country.id,
                    "name": row.name,
                    "created_at": row.created_at.strftime(City.datetime_format),
                    "update_at": row.updated_at.strftime(City.datetime_format)
                })
        else:
            for k, v in city_data.items():
                data.append({
                    "id": v["id"],
                    "country_id": v["country.id"],
                    "name": v["name"],
                    "created_at": datetime.fromtimestamp(v['created_at']),
                    "updated_at": datetime.fromtimestamp(v['updated_at'])
                })

        return jsonify(data), 201

    @staticmethod
    def get_specific_city(city_id):
        """ get specific city by city id """

        city_data = storage.get("City", city_id)

        data = []

        if USE_DB_STORAGE:

            data.append({
                "id": city_data.id,
                "country_id": city_data.country.id,
                "name": city_data.name,
                "created_at": city_data.created_at.strftime(City.datetime_format),
                "update_at": city_data.updated_at.strftime(City.datetime_format)
            })
        else:
            for k, v in city_data.items():
                if city["id"] == city_id:
                    city = storage.get("City", city["id"])
                    data.append({
                        "id": v["id"],
                        "country_id": v["country.id"],
                        "name": v["name"],
                        "created_at": datetime.fromtimestamp(city['created_at']).strftime(city.datetime_format),
                        "updated_at": datetime.fromtimestamp(city['updated_at']).strftime(city.datetime_format)
                    })

        return jsonify(data), 201

    @staticmethod
    def create_new_city():
        """ Create new city """

        if not request.json:
            abort(400, "Request body must be JSON")

        data = request.get_json()

        required_fields = ["country_id", "name"]
        for field in required_fields:
            if field not in data:
                abort(400, f"Missing required field: {field}")

        # # check if country exists, if not, create a new country
        # country_name = data["country_name"]
        # country = storage.get("Country", country_name)

        # if not country:
        #     # Create new country
        #     try:
        #         new_country = Country(name=country_name)
        #         storage.add("Country", new_country)
        #     except ValueError as exc:
        #         abort(400, repr(exc))
        #     country_id = new_country.id
        # else:
        #     country_id = country.id

        # Create new city
        try:
            new_city = City(
                country_id=data["country_id"],
                name=data["name"]
            )
        except ValueError as exc:
            abort(400, repr(exc))

        output = {
            "id": new_city.id,
            "country_id": new_city.country_id,
            "name": new_city.name,
            "created_at": new_city.created_at,
            "updated_at": new_city.updated_at
        }

        try:
            if USE_DB_STORAGE:
                storage.add("City", new_city)
                output["created_at"] = new_city.created_at.strftime(
                    City.datetime_format)
                output["updated_at"] = new_city.updated_at.strftime(
                    City.datetime_format)
            else:
                storage.add("City", output)
                output['created_at'] = datetime.fromtimestamp(
                    new_city.created_at)
                output['updated_at'] = datetime.fromtimestamp(
                    new_city.updated_at)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new City!"

        return jsonify(output), 200

    @staticmethod
    def update_city(city_id):
        """ update specific city by city id """

        if not request.json:
            abort(400, "Request body must be JSON")

        data = request.get_json()

        try:
            result = storage.update("City", city_id, data, [
                                    "country_id", "name"])
        except IndexError as exc:
            print("Error: ", exc)
            abort(404, f"City with ID: {city_id} not found")

        if USE_DB_STORAGE:
            output = {
                "id": result.id,
                "country_id": result.country_id,
                "name": result.name,
                "created_at": result.created_at.strftime(City.datetime_format),
                "updated_at": result.updated_at.strftime(City.datetime_format)
            }
        else:
            output = {
                "id": result["id"],
                "country_id": result["country.id"],
                "name": result["name"],
                "created_at": datetime.fromtimestamp(result["created_at"]),
                "updated_at": datetime.fromtimestamp(result["updated_at"])
            }

        return jsonify(output), 200

    @staticmethod
    def delete_city(city_id):
        """ Deletes an existing city using the specified city ID """

        try:
            storage.delete('City', city_id)
        except IndexError:
            abort(404, description=f"City with ID: {city_id} not found")
        except Exception as e:
            abort(400, description=str(e))

        return jsonify({"message": f"City with ID: {city_id} has been deleted"}), 201
