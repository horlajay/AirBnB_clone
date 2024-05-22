#!/usr/bin/python3
"""
This module defines the Review class.
"""
from models.base_model import BaseModel

class Review(BaseModel):
    """A Review representation.

    Attributes:
        place_id (str): id of the Place.
        user_id (str): id of the User.
        text (str): content of the review.
    """
    place_id = ""
    user_id = ""
    text = ""
