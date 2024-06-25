# city_service.py
#!/usr/bin/python

from datetime import datetime
from flask import jsonify, request, abort
from data import storage, USE_DB_STORAGE
from models.city import City

datetime_format = "%Y-%m-%dT%H:%M:%S.%f"


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

    if not city_id in city_data:
        abort(404, description=f"City with ID: {city_id} not found")

    data = []

    if USE_DB_STORAGE:
        for row in city_data:
            if city.id == city_id:
                city = storage.get("City", city.id)
                data.append({
                    "id": row.id,
                    "country_id": row.country.id,
                    "name": row.name,
                    "created_at": row.created_at.strftime(City.datetime_format),
                    "update_at": row.updated_at.strftime(City.datetime_format)
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


@ staticmethod
def update_city(city_id):
    """ update specific city by city id """

    if not request.json:
        abort(400, "Request body must be JSON")

    data = request.get_json()

    try:
        result = storage.update("City", city_id, data, ["country_id", "name"])
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

    return jsonify({"message": f"City with ID: {city_id} has been deleted"}),
