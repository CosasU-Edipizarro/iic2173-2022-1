import datetime
from typing import Optional
from pydantic import BaseModel as Base
from geoalchemy2 import Geometry


class TokenBase(Base):
    access_token: str
    token_type: str

class TokenData(Base):
    user_id: int
    username: str
    email: str
    name: str
    phone: str
    verified: bool
    uuid: str

class TokenCreate(TokenBase):
    pass

class Token(TokenBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserLoginBase(Base):
    username: str
    password: str

class UserLogin(UserLoginBase):
    pass

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
    uuid: str

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
