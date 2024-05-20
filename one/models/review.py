#!/usr/bin/env python3
"""This script defines a Review class inheriting from BaseModel"""

from models.base_model import BaseModel

class Review(BaseModel):
    """This class handles the instantiation of new Review instances."""

    place_id = ""
    user_id = ""
    text = ""

