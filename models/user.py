#!/usr/bin/python3
"""
This module implements the User class.
"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    User class for managing user information.
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
