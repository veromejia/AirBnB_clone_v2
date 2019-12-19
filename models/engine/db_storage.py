#!/usr/bin/python3
"""DBStorage engine"""

import MySQLdb
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os


class DBStorage:
    """class for DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """Constructor DBStorage"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(user, pwd, host, database),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """return a dictionary with all classes objects in database"""
        my_dict = {}
        if cls:
            result = self.__session.query(eval(cls)).all()
        else:
            new = []
            my_class = ['User', 'State', 'City', 'Review', 'Place', 'Amenity']
            for i in my_class:
                y = self.__session.query(eval(i))
                for j in y:
                    new.append(j)
        for obj in new:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            my_dict[key] = obj
        return my_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database and current database session
        from the engine"""
        self.__session = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)
        Session = scoped_session(self.__session)
        self.__session = Session()
