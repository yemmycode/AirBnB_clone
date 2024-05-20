#!/usr/bin/python3
"""Module for defining the User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """Represents a user."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
