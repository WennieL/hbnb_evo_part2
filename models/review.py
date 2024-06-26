#!/usr/bin/python
""" User model """

from datetime import datetime
import uuid
import re
from flask import jsonify, request, abort
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from data import storage, USE_DB_STORAGE, Base


class Review(Base):
    """Representation of Review """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"

    # Class attrib defaults
    id = None
    __commentor_user_id = ""
    __place_id = ""
    __feedback = ""
    __rating = 0.0
    created_at = None
    updated_at = None

    if USE_DB_STORAGE:
        __tablename__ = 'reviews'
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.now())
        updated_at = Column(DateTime, nullable=False, default=datetime.now())
        __commentor_user_id = Column("commentor_user_id",
                                     String(128), ForeignKey('users.id'), nullable=False)
        __place_id = Column(
            "place_id", String(128), ForeignKey('places.id'), nullable=False)
        __feedback = Column(
            "feedback", String(1024), nullable=False)
        __rating = Column(
            "rating", Integer, nullable=False, default="0.0")
        place = relationship(
            "Place", back_populates="reviews", single_parent=True)
        writer = relationship(
            "User", back_populates="reviews", single_parent=True)

    def __init__(self, *args, **kwargs):
        """Constructor for Review"""
        self.id = str(uuid.uuid4())  # Generate unique ID

        if not USE_DB_STORAGE:
            self.created_at = datetime.now().timestamp()
            self.updated_at = self.created_at

        if kwargs:
            for key, value in kwargs.items():
                if key in ["commentor_user_id", "place_id", "feedback", "rating"]:
                    setattr(self, key, value)

    @property
    def commentor_user_id(self):
        """Getter for commentor_user_id"""
        return self.__commentor_user_id

    @commentor_user_id.setter
    def commentor_user_id(self, value):
        """Setter for commentor_user_id"""
        self.__commentor_user_id = value

    @property
    def place_id(self):
        """Getter for place_id"""
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        """Setter for place_id"""
        self.__place_id = value

    @property
    def feedback(self):
        """Getter for feedback"""
        return self.__feedback

    @feedback.setter
    def feedback(self, value):
        """Setter for feedback"""
        if isinstance(value, str):
            # Trim leading and trailing whitespace
            self.__feedback = value.strip()
        else:
            raise ValueError("Feedback must be a string")

    @property
    def rating(self):
        """Getter for rating"""
        return self.__rating

    @rating.setter
    def rating(self, value):
        """Setter for rating"""
        if isinstance(value, (int, float)) and 0.0 <= value <= 5.0:
            self.__rating = round(value, 2)
        else:
            raise ValueError("Rating must be a number between 0 and 5")

    # # --- Static methods --- removed to servie.review
    @staticmethod
    def all_reviews():
        """ Return all reviews """
        data = []

        try:
            review_data = storage.get('Review')
        except IndexError as exc:
            print("Error: ", exc)
            abort(500, "Unable to load reviews!")

        if USE_DB_STORAGE:
            for row in review_data:
                data.append({
                    "id": row.id,
                    "commentor_user_id": row.commentor_user_id,
                    "place_id": row.place_id,
                    "feedback": row.feedback,
                    "rating": row.rating,
                    "created_at": row.created_at.strftime(Review.datetime_format),
                    "updated_at": row.updated_at.strftime(Review.datetime_format)
                })
        else:
            for k, v in review_data.items():
                data.append({
                    "id": v['id'],
                    "commentor_user_id": v['commentor_user_id'],
                    "place_id": v['place_id'],
                    "feedback": v['feedback'],
                    "rating": v['rating'],
                    "created_at": datetime.fromtimestamp(v['created_at']),
                    "updated_at": datetime.fromtimestamp(v['updated_at'])
                })

        return jsonify(data), 201


# @staticmethod
# def get_specific_review_by_place_id(place_id):
#     """Returns specified reviews of a place"""

#     review_data = storage.get('Review')
#     place_data = storage.get('Place', place_id)

#     if not place_data or place_id not in place_data:
#         abort(404, description=f"Place with ID: {place_id} not found")

#     data = []

#     if USE_DB_STORAGE:
#         for review in review_data:
#             if review.place_id == place_id:
#                 reviewer = storage.get('User', review.commentor_user_id)
#                 data.append({
#                     # Adjust to the correct attribute name
#                     "place_name": place_data[place_id].place_name,
#                     "review": review.feedback,
#                     "rating": f"{review.rating} / 5",
#                     "reviewer": f"{reviewer.first_name} {reviewer.last_name}",
#                     "created_at": review.created_at.strftime(Review.datetime_format),
#                     "updated_at": review.updated_at.strftime(Review.datetime_format)
#                 })
#     else:
#         for review_id, review in review_data.items():
#             if review["place_id"] == place_id:
#                 reviewer = storage.get('User', review["commentor_user_id"])
#                 data.append({
#                     # Adjust to the correct attribute name
#                     "place_name": place_data[place_id]["place_name"],
#                     "review": review["feedback"],
#                     "rating": f"{review['rating']} / 5",
#                     "reviewer": f"{reviewer['first_name']} {reviewer['last_name']}",
#                     "created_at": datetime.fromtimestamp(review['created_at']).strftime(Review.datetime_format),
#                     "updated_at": datetime.fromtimestamp(review['updated_at']).strftime(Review.datetime_format)
#                 })

#     return jsonify(data), 200

    @staticmethod
    def get_specific_review_by_user_id(user_id):
        """Returns specified reviews of a user"""

        review_data = storage.get('Review')
        user_data = storage.get('User', user_id)

        if not user_id in user_data:
            abort(404, description=f"User with ID: {user_id} not found")

        data = []

        if USE_DB_STORAGE:
            for review in review_data:
                if review.commentor_user_id == user_id:
                    reviewer = storage.get('User', review.commentor_user_id)
                    data.append({
                        "place_name": review.place_name,
                        "review": review.feedback,
                        "rating": f"{review.rating} / 5",
                        "reviewer": f"{reviewer.first_name} {reviewer.last_name}",
                        "created_at": review.created_at.strftime(Review.datetime_format),
                        "updated_at": review.updated_at.strftime(Review.datetime_format)
                    })
        else:
            for review_id, review in review_data.items():
                if review["commentor_user_id"] == user_id:
                    reviewer = storage.get('User', review["commentor_user_id"])
                    data.append({
                        "place_name": review["place_name"],
                        "review": review["feedback"],
                        "rating": f"{review['rating']} / 5",
                        "reviewer": f"{reviewer['first_name']} {reviewer['last_name']}",
                        "created_at": datetime.fromtimestamp(review['created_at']).strftime(Review.datetime_format),
                        "updated_at": datetime.fromtimestamp(review['updated_at']).strftime(Review.datetime_format)
                    })

        return jsonify(data), 200


# @staticmethod
# def get_specific_review_by_review_id(review_id):
#     """Returns specified review by review ID"""

#     review_data = storage.get('Review')

#     if not review_data or review_id not in review_data:
#         abort(404, description=f"Review with ID: {review_id} not found")

#     data = []

#     if USE_DB_STORAGE:
#         # Assuming review_data is a list of Review objects
#         for review in review_data:
#             if review.review_id == review_id:
#                 reviewer = storage.get('User', review.commentor_user_id)
#                 data.append({
#                     "place_name": review.place_name,  # Adjust to correct attribute name
#                     "review": review.feedback,
#                     "rating": f"{review.rating} / 5",
#                     "reviewer": f"{reviewer.first_name} {reviewer.last_name}",
#                     "created_at": review.created_at.strftime(Review.datetime_format),
#                     "updated_at": review.updated_at.strftime(Review.datetime_format)
#                 })
#     else:
#         # Assuming review_data is a dictionary where reviews are indexed by review_id
#         if review_id in review_data:
#             review = review_data[review_id]
#             reviewer = storage.get('User', review["commentor_user_id"])
#             data.append({
#                 # Adjust to correct attribute name
#                 "place_name": review["place_name"],
#                 "review": review["feedback"],
#                 "rating": f"{review['rating']} / 5",
#                 "reviewer": f"{reviewer['first_name']} {reviewer['last_name']}",
#                 "created_at": datetime.fromtimestamp(review['created_at']).strftime(Review.datetime_format),
#                 "updated_at": datetime.fromtimestamp(review['updated_at']).strftime(Review.datetime_format)
#             })

#     return jsonify(data), 200


    @staticmethod
    def create_new_review(place_id):
        """Creates a new review for the specified place"""

        if not request.json:
            abort(400, "Request body must be JSON")

        data = request.get_json()

        required_fields = ["commentor_user_id",
                           "place_id", "feedback", "rating"]
        for field in required_fields:
            if field not in data:
                abort(400, f"Missing required field: {field}")

        if data["place_id"] != place_id:
            abort(400, "Mismatched place_id in URL and data")

        try:
            new_review = Review(
                commentor_user_id=data["commentor_user_id"],
                place_id=data["place_id"],
                feedback=data["feedback"],
                rating=data["rating"]
            )
        except ValueError as exc:
            abort(400, repr(exc))

        output = {
            "id": new_review.id,
            "commentor_user_id": new_review.commentor_user_id,
            "place_id": new_review.place_id,
            "feedback": new_review.feedback,
            "rating": new_review.rating,
            "created_at": new_review.created_at,
            "updated_at": new_review.updated_at
        }

        try:
            if USE_DB_STORAGE:
                storage.add('Review', new_review)
                output['created_at'] = new_review.created_at.strftime(
                    Review.datetime_format)
                output['updated_at'] = new_review.updated_at.strftime(
                    Review.datetime_format)
            else:
                storage.add('Review', output)
                output['created_at'] = datetime.fromtimestamp(
                    new_review.created_at)
                output['updated_at'] = datetime.fromtimestamp(
                    new_review.updated_at)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Place!"

        return jsonify(output), 200

    @staticmethod
    def update_review(place_id):
        """update exisitng review by place_id"""

        if not request.json:
            abort(400, "Request body must be JSON")

        data = request.get_json()

        try:
            result = storage.update('Review', place_id, data, [
                "feedback", "rating"])

        except IndexError as exc:
            print("Error: ", exc)
            abort(404, f"Review with ID: {place_id} not found")

        if USE_DB_STORAGE:
            output = {
                "id": result.id,
                "commentor_user_id": result.commentor_user_id,
                "place_id": result.place_id,
                "feedback": result.feedback,
                "rating": result.rating,
                "created_at": result.created_at.strftime(Review.datetime_format),
                "updated_at": result.updated_at.strftime(Review.datetime_format)
            }
        else:
            output = {
                "id": result["id"],
                "commentor_user_id": result["commentor_user_id"],
                "place_id": result["place_id"],
                "feedback": result["feedback"],
                "rating": result["rating"],
                "created_at": datetime.fromtimestamp(result["created_at"]),
                "updated_at": datetime.fromtimestamp(result["updated_at"])
            }

        return jsonify(output), 200

    @staticmethod
    def delete_review(review_id):
        """Deletes an existing review using the specified review ID"""

        try:
            storage.delete('Review', review_id)
        except IndexError:
            abort(404, description=f"Review with ID: {review_id} not found")
        except Exception as e:
            abort(400, description=str(e))

        return jsonify({"message": f"Review with ID: {review_id} has been deleted"}),
