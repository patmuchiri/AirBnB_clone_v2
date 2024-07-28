#!/usr/bin/python3
""" This module manages MySQL Database """

import os

from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

user = os.getenv('HBNB_MYSQL_USER')
password = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
db_name = os.getenv('HBNB_MYSQL_DB')
env = os.getenv('HBNB_ENV')


class DBStorage:
    """ Defines a database storage instance """

    __engine = None
    __session = None
    __classes = [State, City, User, Place, Review, Amenity]

    def __init__(self):
        """ Instantiates the DBStorage """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, password, host, db_name), pool_pre_ping=True)

        if env == "test":
            Base.Metadata.drop_all()

    def all(self, cls=None):
        """ query on the current database session on
            all objects depending of the class name
        """
        query_results = {}
        if cls in self.__classes:
            result = DBStorage.__session.query(cls)
            for row in result:
                key = "{}.{}".format(row.__class__.__name__, row.id)
                query_results[key] = row
        elif cls is None:
            for cl in self.__classes:
                result = DBStorage.__session.query(cl)
                for row in result:
                    key = "{}.{}".format(row.__class__.__name__, row.id)
                    query_results[key] = row

        return query_results

    def new(self, obj):
        """  add the object to the current database session """
        DBStorage.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session """
        DBStorage.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not none"""
        DBStorage.__session.delete(obj)

    def reload(self):
        """ Creates the current database session """
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)

        DBStorage.__session = Session()

    def close(self):
        """ call close() method on the private session
        attribute (self.__session)
        """
        DBStorage.__session.close()
