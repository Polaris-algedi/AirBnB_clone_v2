#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class City(BaseModel, Base):
    """
    The City class inherits from BaseModel and Base. It represents a city
    with its associated properties and methods. The class has a relationship
    with the Place class.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store cities.
        name (str): The name of the city. It's a required field in db mode.
        state_id (str): The id of the state the city belongs to.
        It's a required field in db mode.
        places (list): A list of Place instances associated with the city.

    """
    __tablename__ = "cities"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', cascade='all, delete', backref='cities')
    else:
        name = ""
        state_id = ""
