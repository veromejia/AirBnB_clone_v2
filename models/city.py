#!/usr/bin/python3
"""This is the city class"""
from models.base_model import BaseModel


Base = declarative_base()


class City(BaseModel):
    """This is the class for City
    Attributes:
        state_id: The state id
        name: input name
    """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(string(60), nullable=False, ForeignKey('states.id'))
