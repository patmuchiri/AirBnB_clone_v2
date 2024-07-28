#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete-orphan")

    @property
    def cities(self):
        """getter attribute cities that returns the list of City
           instances with state_id equals to the current State.id
        """
        from models import storage
        cities_list = []

        cities = storage.all(City).value()
        for city in cities:
            if self.id == city.state_id:
                cities_list.append(city)

        return cities_list
