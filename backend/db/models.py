import datetime
from email.policy import default
from operator import index

from sqlalchemy import Column, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry, Geography

from db.engine import db_init
from db.db_utils import load_env


# Import .env
ENV = load_env()

# Initialize Database
db = db_init(ENV['DATABASE_URI'], ENV['DEBUG'])

engine = db['engine']
Session = db['Session']
Base = db['Base']

# Dependency
def get_db():
    print("get_db(): Starting")
    db = Session()
    try:
        print("get_db(): Yielding")
        yield db
    finally:
        print("get_db(): Closing")
        db.close()


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True, index=True)
    auth_id = Column(Integer(), nullable=False)
    # name = Column(Text(), nullable=False)
    # username = Column(Text(), unique=True, nullable=False)
    # email = Column(Text(), unique=True, nullable=False)
    # phone = Column(Text(), unique=True)
    # password = Column(Text(), nullable=False)
    # verified = Column(Boolean(), default=False)

    # jwt = relationship("JWT", back_populates="user", uselist=False)
    locations = relationship("Location", back_populates="user")


class Location(Base):

    __tablename__ = 'locations'

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(Text(), nullable=False)
    coords = Column(Geometry(geometry_type='POINT', srid=4326))
    tag = Column(Text(), nullable=False)

    user_id = Column(Integer(), ForeignKey('users.id'), index=True) #auth_id?
    user = relationship("User", back_populates="locations")


# class JWT(Base):

#     __tablename__ = 'jwts'

#     id = Column(Integer, primary_key=True, index=True)
#     token = Column(Text(), nullable=False, index=True)

#     user_id = Column(Integer(), ForeignKey('users.id'), index=True)
#     user = relationship("User", back_populates="jwt")


class Ping(Base):

    __tablename__ = 'pings'
    
    id = Column(Integer, primary_key=True, index=True)

    sender_id = Column(Integer(), ForeignKey('users.id'), index=True)
    receiver_id = Column(Integer(), ForeignKey('users.id'), index=True)
    sidi = Column(Float(), default=0)
    siin = Column(Float(), default=0)
    dindin = Column(Float(), default=0)
    accepted = Column(Boolean(), default=False)


# class VerificationEmail(Base):

#     __tablename__ = 'verification_emails'

#     id = Column(Integer, primary_key=True, index=True)
#     token = Column(Text(), nullable=False, index=True)

#     user_id = Column(Integer(), ForeignKey('users.id'), index=True)
#     user = relationship("User")