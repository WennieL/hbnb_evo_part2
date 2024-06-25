#!/usr/bin/python
""" Review model """

from datetime import datetime
import uuid
import re
from flask import jsonify, request, abort
from sqlalchemy import Column, String, DateTime
from data import storage, USE_DB_STORAGE, Base


class Review(Base):
    """Representation of review """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"

    if USE_DB_STORAGE:
        __tablename__ = 'reviews'
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.now())
        updated_at = Column(DateTime, nullable=False, default=datetime.now())
        __commentor_user_id = Column(
            "commentor_user_id", String(128), nullable=False, default="")
        __place_id = Column(
            "place_id", String(128), nullable=False, default="")
        __feedback = Column(
            "feedback", String(256), nullable=False, default="")
        __rating = Column(
            "rating", String(60), nullable=False, default="0.0")

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

    # # --- Static methods --- removed to review_service
    # @staticmethod
    # def all_reviews():
    #     """ Return all reviews """

    #     data = []

    #     try:
    #         review_data = storage.get('Review')
    #     except IndexError as exc:
    #         print("Error: ", exc)
    #         return "Unable to load reviews!", 500

    #     if USE_DB_STORAGE:
    #         for row in review_data:
    #             reviewer_name = row.commentor_user_id  # Default to user ID if no name found
    #             if row.commentor_user_id:
    #                 reviewer = storage.get('User', row.commentor_user_id)
    #                 reviewer_name = f"{reviewer.first_name} {reviewer.last_name}"

    #             data.append({
    #                 "review": row.feedback,
    #                 "rating": f"{row.rating} / 5",
    #                 "reviewer_name": reviewer_name,
    #                 "created_at": row.created_at.strftime(Review.datetime_format),
    #                 "updated_at": row.updated_at.strftime(Review.datetime_format)
    #             })
    #     else:
    #         for review_id, review_value in review_data.items():
    #             # Default to user ID if no name found
    #             reviewer_name = review_value["commentor_user_id"]
    #             reviewer = storage.get(
    #                 'User', review_value["commentor_user_id"])
    #             reviewer_name = f"{reviewer.first_name} {reviewer.last_name}"

    #             data.append({
    #                 "review_place_id": review_value["place_id"],
    #                 "place_name": storage.get('Place', review_value["place_id"]).name,
    #                 "reviewer_name": reviewer_name,
    #                 "created_at": datetime.fromtimestamp(review_value['created_at']),
    #                 "updated_at": datetime.fromtimestamp(review_value['updated_at'])
    #             })

    #     return jsonify(data), 200

    # @staticmethod
    # def get_specific_review_by_place_id(place_id):
    #     """Returns specified reviews of a place"""

    #     review_data = storage.get('Review')
    #     place_data = storage.get('Place')
    #     user_data = storage.get('User')

    #     reviewer_data = {}

    #     for review_value in review_data.values():
    #         if review_value["place_id"] == place_id:
    #             review_place_id = review_value["place_id"]
    #             place_name = place_data[review_place_id]["name"]
    #             commentor_id = review_value["commentor_user_id"]
    #             reviewer_first_name = user_data[commentor_id]["first_name"]
    #             reviewer_last_name = user_data[commentor_id]["last_name"]

    #             if place_name not in reviewer_data:
    #                 reviewer_data[place_name] = []

    #             reviewer_data[place_name].append({
    #                 "review": review_value["feedback"],
    #                 "rating": f"{review_value['rating']} / 5",
    #                 "reviewer": f"{reviewer_first_name} {reviewer_last_name}",
    #                 "created_at": datetime.fromtimestamp(review_value['created_at']).isoformat(),
    #                 "updated_at": datetime.fromtimestamp(review_value['updated_at']).isoformat()
    #             })

    #     if not reviewer_data:
    #         abort(
    #             404, description=f"No reviews found for place with ID: {place_id}")

    #     return jsonify(reviewer_data), 200

    # @staticmethod
    # def get_specific_review_by_user_id(user_id):
    #     """Returns specified reviews of a user"""

    #     # Assuming review_data, place_data, and user_data are fetched from your data storage
    #     review_data = storage.get('Review')
    #     place_data = storage.get('Place')
    #     user_data = storage.get('User')

    #     if not user_id in user_data:
    #         abort(404, description=f"User with ID: {user_id} not found")

    #     reviews = []

    #     # Iterate through review_data to find reviews matching user_id
    #     for review_value in review_data.values():
    #         if review_value["commentor_user_id"] == user_id:
    #             review_place_id = review_value["place_id"]
    #             place_name = place_data[review_place_id]["name"]
    #             reviewer_first_name = user_data[user_id]["first_name"]
    #             reviewer_last_name = user_data[user_id]["last_name"]

    #             reviews.append({
    #                 "place_name": place_name,
    #                 "review": review_value["feedback"],
    #                 "rating": f"{review_value['rating']} / 5",
    #                 "reviewer": f"{reviewer_first_name} {reviewer_last_name}",
    #                 "created_at": datetime.fromtimestamp(review_value['created_at']).isoformat(),
    #                 "updated_at": datetime.fromtimestamp(review_value['updated_at']).isoformat()
    #             })

    #     if not reviews:
    #         abort(
    #             404, description=f"No reviews found for user with ID: {user_id}")

    #     return jsonify(reviews), 200

    # @staticmethod
    # def get_specific_review_by_review_id(review_id):
    #     """Returns specified review by review ID"""

    #     review_data = storage.get('Review')
    #     place_data = storage.get('Place')
    #     user_data = storage.get('User')

    #     if review_id not in review_data:
    #         abort(404, description=f"Review with ID: {review_id} not found")

    #     review_value = review_data[review_id]
    #     review_place_id = review_value["place_id"]
    #     place_name = place_data[review_place_id]["name"]
    #     commentor_id = review_value["commentor_user_id"]
    #     reviewer_first_name = user_data[commentor_id]["first_name"]
    #     reviewer_last_name = user_data[commentor_id]["last_name"]

    #     review_details = {
    #         "place_name": place_name,
    #         "review": review_value["feedback"],
    #         "rating": f"{review_value['rating']} / 5",
    #         "reviewer": f"{reviewer_first_name} {reviewer_last_name}",
    #         "created_at": datetime.fromtimestamp(review_value['created_at']).isoformat(),
    #         "updated_at": datetime.fromtimestamp(review_value['updated_at']).isoformat()
    #     }

    #     return jsonify(review_details), 200

    # @staticmethod
    # def create_new_review(place_id):
    #     """Creates a new review for the specified place"""

    #     if not request.json:
    #         abort(400, description="Request does not contain valid JSON data")

    #     data = request.json
    #     required_fields = ['commentor_user_id', 'feedback', 'rating']

    #     for field in required_fields:
    #         if field not in data:
    #             abort(400, description=f"Missing required field: {field}")

    #     commentor_user_id = data['commentor_user_id']
    #     feedback = data['feedback']
    #     rating = data['rating']

    #     try:
    #         new_review = Review(
    #             commentor_user_id=commentor_user_id,
    #             place_id=place_id,
    #             feedback=feedback,
    #             rating=rating
    #         )
    #     except ValueError as e:
    #         abort(400, description=str(e))

    #     new_review.id = str(uuid.uuid4())
    #     new_review.created_at = datetime.now()
    #     new_review.updated_at = new_review.created_at

    #     storage.add('Review', new_review)

    #     response_data = {
    #         "id": new_review.id,
    #         "place_id": place_id,
    #         "commentor_user_id": commentor_user_id,
    #         "feedback": feedback,
    #         "rating": f"{new_review.rating} / 5",
    #         "created_at": new_review.created_at.isoformat(),
    #         "updated_at": new_review.updated_at.isoformat()
    #     }

    #     return jsonify(response_data), 201

    # @staticmethod
    # def update_review(place_id):
    #     """Updates an existing review using the specified place ID"""

    #     if not request.json:
    #         abort(400, description="Request does not contain valid JSON data")

    #     review_id = request.json.get('id')
    #     if not review_id:
    #         abort(400, description="Missing review ID")

    #     try:
    #         review = storage.get('Review', review_id)
    #     except IndexError:
    #         abort(404, description=f"Review with ID: {review_id} not found")

    #     if review.place_id != place_id:
    #         abort(
    #             400, description=f"Review with ID: {review_id} does not belong to place with ID: {place_id}")

    #     allowed_fields = ['feedback', 'rating']

    #     # Update review object with request data using setattr in a loop
    #     for field, value in request.json.items():
    #         if field in allowed_fields:
    #             setattr(review, field, value)

    #     try:
    #         updated_review = storage.update_review(review)
    #     except Exception as e:
    #         abort(500, description=f"Failed to update review: {str(e)}")

    #     response_data = {
    #         "id": updated_review.id,
    #         "place_id": updated_review.place_id,
    #         "commentor_user_id": updated_review.commentor_user_id,
    #         "feedback": updated_review.feedback,
    #         "rating": f"{updated_review.rating} / 5",
    #         "created_at": updated_review.created_at.isoformat(),
    #         "updated_at": updated_review.updated_at.isoformat()
    #     }

    #     return jsonify(response_data), 200

    # @staticmethod
    # def delete_review(review_id):
    #     """Deletes an existing review using the specified review ID"""
    #     try:
    #         storage.delete('Review', review_id)
    #     except IndexError:
    #         abort(404, description=f"Review with ID: {review_id} not found")
    #     except Exception as e:
    #         abort(400, description=str(e))

    #     return jsonify({"message": f"Review with ID: {review_id} has been deleted"}), 200
