import datetime
from operator import index

from sqlalchemy import Column, Integer, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from db.engine import db_init
from db.db_utils import load_env


# Import .env
ENV = load_env()

# Initialize Database
db = db_init(ENV['DATABASE_URI'])

engine = db['engine']
Session = db['Session']
Base = db['Base']

# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(Text(), nullable=False)
    username = Column(Text(), unique=True, nullable=False)
    email = Column(Text(), unique=True, nullable=False)
    phone = Column(Text(), unique=True)
    instagram = Column(Text(), unique=True)
    sex = Column(Text())
    password = Column(Text(), nullable=False)

    jwt = relationship("JWT", back_populates="user", uselist=False)
    locations = relationship("Location", back_populates="user")


class Location(Base):

    __tablename__ = 'locations'

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(Text(), nullable=False)
    coords = Column(Geometry(geometry_type='POINT', srid=4326))

    user_id = Column(Integer(), ForeignKey('users.id'), index=True)
    user = relationship("User", back_populates="locations")


class JWT(Base):

    __tablename__ = 'jwts'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text(), nullable=False, index=True)

    created = Column(DateTime(), default=datetime.datetime.utcnow)
    duration = Column(Integer(), default=3600)

    user_id = Column(Integer(), ForeignKey('users.id'), index=True)
    user = relationship("User", back_populates="jwt")
