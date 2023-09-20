#!/usr/bin/python3
"""
This module defines the DBStorage class which manages persistent storage
for the hbnb clone using a MySQL database.
"""
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """
    This class manages SQL database storage for hbnb clone. It creates and
    manages the engine and session for the database.

    Attributes:
        __engine (sqlalchemy.Engine): The SQLAlchemy engine.
        __session (sqlalchemy.orm.session.Session): The SQLAlchemy session.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes DBStorage instance, creates the engine and connects to
        the database.
        """
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env0 = getenv("HBNB_ENV", "none")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)

        if env0 == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of all objects of a given class, if specified,
        or all objects in the database if no class is specified.

        Args:
            cls (str, optional): The class of the objects to return.

        Returns:
            dict: A dictionary of all objects, with the key as the class name
            and id of the object, and the value as the object itself.
        """
        dic = {}
        if cls:
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                dic[key] = obj
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for clas in classes:
                query = self.__session.query(clas)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    dic[key] = obj
        return (dic)

    def new(self, obj):
        """
        Adds an object to the current database session.

        Args:
            obj (BaseModel): The object to add.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session to the database.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the current database session.

        Args:
            obj (BaseModel, optional): The object to delete.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates the current database session from the engine using a
        sessionmaker.
        """
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        """
        Closes the current database session.
        """
        self.__session.close()
