#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True,
                             nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship("Amenity", secondary=place_amenity,
                             viewonly=False)

    @property
    def reviews(self):
        """ for FileStorage: getter attribute reviews that returns the list
            of Review instances with place_id equals to the current Place.id
            It will be the FileStorage relationship between Place and Review
        """
        from models import storage

        reviews_list = []
        review_instances = storage.all('Review').values()

        for review in review_instances:
            if self.id == review.place_id:
                reviews_list.append(review)
        return reviews_list

    @property
    def amenities(self):
        """ Getter attribute that returns the list of Amenity instances
            based on the attribute amenity_ids,
            that contains all Amenity.id linked to the Place
        """
        from models import storage
        amenities_list = []
        amenity_instances = storage.all('Amenity').values()

        for amenity in amenity_instances:
            if self.id == amenity.amenity_ids:
                amenities_list.append(amenity)
        return amenities_list

    @amenities.setter
    def amenities(self, obj):
        """ Handles append method for adding an Amenity.id to the
            attribute amenity_ids.
        """
        if isinstance(obj, "Amenity"):
            self.amenity_id.append(obj.id)
