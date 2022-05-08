import datetime
from typing import Optional
from pydantic import BaseModel as Base


class JWTBase(Base):
    token: str
    created: Optional[str] = datetime.datetime.utcnow().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    duration: Optional[int] = 3600


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
    instagram: str
    sex: str
    verified: bool


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    # jwt: Optional[JWT]
    # locations: Optional[list[Location]]

    class Config:
        orm_mode = True


class PingBase(Base):
    seen: bool
    created_at: Optional[str] = datetime.datetime.utcnow().strftime("%d-%b-%Y (%H:%M:%S.%f)")


class PingCreate(PingBase):
    pass


class Ping(PingBase):
    id: int
    sender_id: int
    receiver_id: int

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