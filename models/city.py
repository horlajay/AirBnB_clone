#!/usr/bin/python3
"""
This module defines the City class.
"""
from models.base_model import BaseModel

class City(BaseModel):
    """
    A class to represent a city.

    Attributes:
        state_id (str): id of the state.
        name (str): name of the city.
    """

    state_id = ""
    name = ""
