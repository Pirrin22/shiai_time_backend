from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base

# =============================================
# 1. TABLAS INTERMEDIAS (Many-to-Many)
# =============================================

usuario_dojo = Table(
    'usuario_dojo', Base.metadata,
    Column('user_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('dojo_id', Integer, ForeignKey('dojos.id'), primary_key=True)
)

usuario_arte_marcial = Table(
    'usuario_arte_marcial', Base.metadata,
    Column('user_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('martial_art_id', Integer, ForeignKey('artes_marciales.id'), primary_key=True)
)

dojo_arte_marcial = Table(
    'dojo_arte_marcial', Base.metadata,
    Column('dojo_id', Integer, ForeignKey('dojos.id'), primary_key=True),
    Column('martial_art_id', Integer, ForeignKey('artes_marciales.id'), primary_key=True)
)

# Tabla "Self-Referential" para el sistema de seguidores
seguidores = Table(
    'seguidores', Base.metadata,
    Column('follower_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('usuarios.id'), primary_key=True)
)

# =============================================
# 2. MODELOS PRINCIPALES
# =============================================

class User(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name_1 = Column(String)
    last_name_2 = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    email = Column(String, unique=True, index=True)
    password = Column(String)
    profile_picture = Column(String, nullable=True)
    belt = Column(String, nullable=True)

    ranking_points = Column(Integer, default=0)
    classes_taken = Column(Integer, default=0)
    total_fights = Column(Integer, default=0)

    # FKs de localización
    country_id = Column(Integer, ForeignKey('paises.id'), nullable=True)
    region_id = Column(Integer, ForeignKey('regiones.id'), nullable=True)
    city = Column(String, nullable=True)

    # Relaciones Dinámicas (ORM)
    dojos = relationship('Dojo', secondary=usuario_dojo, back_populates='users')
    martial_arts = relationship('MartialArts', secondary=usuario_arte_marcial, back_populates='users')

    # Red de Seguidores y seguidos

    following = relationship(
        'User',
        secondary=seguidores,
        primaryjoin=id==seguidores.c.follower_id,
        secondaryjoin=id==seguidores.c.followed_id,
        backref='followers'
    )

class Dojo(Base):
    __tablename__ = 'dojos'

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)

    # Relaciones Dinámicas (ORM)
    users = relationship('User', secondary=usuario_dojo, back_populates='dojos')
    martial_arts = relationship('MartialArts', secondary=dojo_arte_marcial, back_populates='dojos')

class MartialArts(Base):
    __tablename__ = 'artes_marciales'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relaciones Dinámicas (ORM)
    users = relationship('User', secondary=usuario_arte_marcial, back_populates='martial_arts')
    dojos = relationship('Dojo', secondary=dojo_arte_marcial, back_populates='martial_arts')
# =============================================
# 3. MODELOS DE LOCALIZACIÓN
# =============================================

class Country(Base):
    __tablename__ = 'paises'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Region(Base):
    __tablename__ = 'regiones'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country_id = Column(Integer, ForeignKey('paises.id'))