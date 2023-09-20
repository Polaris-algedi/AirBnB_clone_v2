#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from os import getenv

place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False,
    ),
)


class Place(BaseModel, Base):
    """A place to stay"""

    __tablename__ = "places"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        reviews = relationship("Review", backref="place", cascade="delete")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False)

    else:
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

        @property
        def reviews(self):
            from models.__init__ import storage
            from models.review import Review

            review_list = []
            all_reviews = storage.all(Review)
            for review in all_reviews:
                if self.id == review.place_id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            from models.__init__ import storage
            from models.amenity import Amenity

            amenity_list = []
            all_amenities = storage.all(Amenity)
            for amenity in all_amenities:
                if self.id == amenity.place_id:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            from models.__init__ import storage
            from models.amenity import Amenity

            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
