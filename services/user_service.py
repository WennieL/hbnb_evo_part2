#!/usr/bin/python

from datetime import datetime
import uuid
from flask import jsonify, request, abort
from data import storage, USE_DB_STORAGE
from models.user import User

datetime_format = "%Y-%m-%dT%H:%M:%S.%f"


@staticmethod
def all_users():
    """ Class method that returns all users data"""
    data = []

    try:
        user_data = storage.get('User')
    except IndexError as exc:
        print("Error: ", exc)
        return "Unable to load users!"

    if USE_DB_STORAGE:
        # DBStorage
        for row in user_data:
            # use print(row.__dict__) to see the contents of the sqlalchemy model objects
            data.append({
                "id": row.id,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "email": row.email,
                "password": row.password,
                "created_at": row.created_at.strftime(User.datetime_format),
                "updated_at": row.updated_at.strftime(User.datetime_format)
            })
    else:
        # FileStorage
        for k, v in user_data.items():
            data.append({
                "id": v['id'],
                "first_name": v['first_name'],
                "last_name": v['last_name'],
                "email": v['email'],
                "password": v['password'],
                "created_at": datetime.fromtimestamp(v['created_at']),
                "updated_at": datetime.fromtimestamp(v['updated_at'])
            })

    return jsonify(data), 201


@staticmethod
def specific(user_id):
    """ Class method that returns a specific user's data"""
    data = []

    try:
        user_data = storage.get('User', user_id)
    except IndexError as exc:
        print("Error: ", exc)
        return "User not found!"

    if USE_DB_STORAGE:
        # DBStorage
        data.append({
            "id": user_data.id,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "password": user_data.password,
            "created_at": user_data.created_at.strftime(User.datetime_format),
            "updated_at": user_data.updated_at.strftime(User.datetime_format)
        })
    else:
        # FileStorage
        data.append({
            "id": user_data['id'],
            "first_name": user_data['first_name'],
            "last_name": user_data['last_name'],
            "email": user_data['email'],
            "password": user_data['password'],
            "created_at": datetime.fromtimestamp(user_data['created_at']),
            "updated_at": datetime.fromtimestamp(user_data['updated_at'])
        })
    return jsonify(data)


@staticmethod
def create():
    """ Class method that creates a new user"""
    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()

    required_fields = ['first_name', 'last_name', 'email', 'password']
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing {field}")
    # Validate email format (basic check)
    if not "@" in data["email"]:
        abort(400, "Invalid email format")

    # Check if email is already in use
    if USE_DB_STORAGE:
        try:
            existing_user = storage.get('User', data['email'])
            if existing_user:
                abort(400, "Email already in use")
        except IndexError:
            pass

    try:
        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"]
        )
    except ValueError as exc:
        return repr(exc) + "\n"

    output = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "created_at": new_user.created_at,
        "updated_at": new_user.updated_at
    }

    try:
        if USE_DB_STORAGE:
            # DBStorage - note that the add method uses the User object instance 'new_user'
            storage.add('User', new_user)
            # datetime -> readable text
            output['created_at'] = new_user.created_at.strftime(
                User.datetime_format)
            output['updated_at'] = new_user.updated_at.strftime(
                User.datetime_format)
        else:
            # FileStorage - note that the add method uses the dictionary 'output'
            storage.add('User', output)
            # timestamp -> readable text
            output['created_at'] = datetime.fromtimestamp(
                new_user.created_at)
            output['updated_at'] = datetime.fromtimestamp(
                new_user.updated_at)
    except IndexError as exc:
        print("Error: ", exc)
        return "Unable to add new User!"
    return jsonify(output)


@staticmethod
def update(user_id):
    """ Class method that updates an existing user"""
    if request.get_json() is None:
        abort(400, "Not a JSON")

    data = request.get_json()

    try:
        # update the User record. Only first_name and last_name can be changed
        result = storage.update('User', user_id, data, [
                                "first_name", "last_name"])
    except IndexError as exc:
        print("Error: ", exc)
        return "Unable to update specified user!"

    if USE_DB_STORAGE:
        output = {
            "id": result.id,
            "first_name": result.first_name,
            "last_name": result.last_name,
            "email": result.email,
            "created_at": result.created_at.strftime(User.datetime_format),
            "updated_at": result.updated_at.strftime(User.datetime_format)
        }
    else:
        output = {
            "id": result["id"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "email": result["email"],
            "created_at": datetime.fromtimestamp(result["created_at"]),
            "updated_at": datetime.fromtimestamp(result["updated_at"])
        }
    # print out the updated user details
    return jsonify(output), 200


@staticmethod
def delete(user_id):
    """Deletes an existing user using the specified user ID"""

    try:
        storage.delete('User', user_id)
    except IndexError:
        abort(404, description=f"User with ID: {user_id} not found")
    except Exception as e:
        abort(400, description=str(e))

    return jsonify({"message": f"User with ID: {user_id} has been deleted"}), 200
