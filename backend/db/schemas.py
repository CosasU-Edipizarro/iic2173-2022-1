import datetime
from typing import Optional
from pydantic import BaseModel as Base
from geoalchemy2 import Geometry

class JWTBase(Base):
    token: str


class JWTCreate(JWTBase):
    pass


class JWT(JWTBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class LocationBase(Base):
    name: str
    coords: str


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
    password: str


class User(UserBase):
    id: int
    verified: bool
    # jwt: Optional[JWT]
    # locations: Optional[list[Location]]

    class Config:
        orm_mode = True


class PingBase(Base):
    seen: bool
    created_at: Optional[str] = str(datetime.datetime.utcnow().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
    sender_id: int
    receiver_id: int


class PingCreate(PingBase):
    pass


class Ping(PingBase):
    id: int

    class Config:
        orm_mode = True


class VerificationEmailBase(Base):
    pass

class VerificationEmailCreate(VerificationEmailBase):
    pass

class VerificationEmail(VerificationEmailBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True



class CountBase(Base):
    count: int

class Count(CountBase):
    pass


# class LocationPointBase(Base):
#     name: str
#     coords: Types.Point


# class LocationPointCreate(LocationPointBase):
#     pass


# class LocationPoint(LocationPointBase):
#     id: int
#     user_id: int
