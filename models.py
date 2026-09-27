from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    # Aquí definimos las columnas.

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    profile_picture = Column(String)
    belt = Column(String)
    ranking_points = Column(Integer, default=0)
    classes_taken = Column(Integer, default=0)
    total_fights = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
