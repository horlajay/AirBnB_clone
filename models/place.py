#!/usr/bin/python3
"""
This module defines the Place class.
"""
from models.base_model import BaseModel


class Place(BaseModel):
    """A class to represent a place.

    Attributes:
        city_id (str): id of the city.
        user_id (str): id of the user.
        name (str): name of the place.
        description (str): description of the place.
        number_rooms (int): number of rooms in the place.
        number_bathrooms (int): number of bathrooms in the place.
        max_guest (int): maximum number of guests the place can accommodate.
        price_by_night (int): price per night for the place.
        latitude (float): latitude coordinate of the place.
        longitude (float): longitude coordinate of the place.
        amenity_ids (list): list of ids for amenities provided.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
