import re
from uuid import uuid4 as uuid

import bcrypt
from fastapi import Header, HTTPException

from db.models import Session, User, JWT, Location
from db import schemas

def generate_unique(req_type='hex') -> str:
    if req_type == 'str':
        data = str(uuid())
    elif req_type == 'int':
        data = uuid().int
    elif req_type == 'hex':
        data = uuid().hex
    else:
        data = uuid()
    return data


def verify_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else:
        return False


def verify_password_hash(password: str, password_hash: str) -> bool:
    password = password.encode()
    return bcrypt.check_password_hash(password_hash, password)


def generate_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


async def get_query_token(db: Session, token: str):
    token = db.query(JWT).filter(JWT.token == token).first()
    if not token:
        raise HTTPException(status_code=400, detail="Invalid token")


async def get_token_header(db: Session, x_token: str = Header(...)):
    x_token = db.query(JWT).filter(JWT.token == x_token).first()
    if not x_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
