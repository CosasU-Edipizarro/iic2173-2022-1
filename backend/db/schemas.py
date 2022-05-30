import datetime
from typing import Optional
from pydantic import BaseModel as Base
from geoalchemy2 import Geometry


class TokenBase(Base):
    access_token: str
    token_type: str

# class JWTBase(Base):
#     token: str


# class JWTCreate(JWTBase):
#     pass

# class JWT(JWTBase):
#     id: int
#     user_id: int

#     class Config:
#         orm_mode = True


class LocationBase(Base):
    name: str
    coords: str
    tag: str


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(Base):
    name: str
    username: str
    email: str
    phone: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    verified: bool


class PingBase(Base):
    sender_id: int
    receiver_id: int


class PingCreate(PingBase):
    pass


class Ping(PingBase):
    id: int
    sidi: float
    siin: float
    dindin: float

    class Config:
        orm_mode = True


# class VerificationEmailBase(Base):
#     pass

# class VerificationEmailCreate(VerificationEmailBase):
#     pass

# class VerificationEmail(VerificationEmailBase):
#     id: int
#     user_id: int

#     class Config:
#         orm_mode = True

class UserLoginBase(Base):
    username: str
    password: str

class UserLogin(UserLoginBase):
    pass

class CountBase(Base):
    count: int

class Count(CountBase):
    pass
