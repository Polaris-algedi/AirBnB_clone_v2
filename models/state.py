#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """
    The State class inherits from BaseModel and Base. It represents a state
    with its associated properties and methods. The class has a relationship
    with the City class.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store states.
        name (str): The name of the state. It's a required field in db mode.
        cities (list): A list of City instances associated with the state.

    Properties:
        cities: In file storage mode, this property returns a list of City
        instances where the state_id matches the current State instance id.
    """
    __tablename__ = "states"
    if getenv('HBNB_TYPE_STORAGE') == "db":
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade='all, delete', backref='state')
    else:
        name = ""

        @property
        def cities(self):
            from models.__init__ import storage
            from models.city import City
            city_list = []
            storage_data = storage.all(City)
            for city in storage_data.values():
                if self.id == city.state_id:
                    city_list.append(city)
            return city_list
