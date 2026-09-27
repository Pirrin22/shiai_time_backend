from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class User(Base):
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
    country_id = Column(Integer, ForeignKey('paises.id'), nullable=True)
    region_id = Column(Integer, ForeignKey('regiones.id'), nullable=True)
    city = Column(String, nullable=True)

class Country(Base):
    __tablename__ = 'paises'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Region(Base):
    __tablename__ = 'regiones'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country_id = Column(Integer, ForeignKey('paises.id'))