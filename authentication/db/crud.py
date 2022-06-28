import datetime
from fastapi import HTTPException, Depends, status
from typing import Union

from datetime import datetime, timedelta

from db.models import ENV, Session, User, VerificationEmail, Token, get_db
from db import schemas
from dependencies import utils

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

ALGORITHM=ENV["ALGORITHM"]
SECRET_KEY=ENV["SECRET_KEY"]
ACCESS_TOKEN_EXPIRE_MINUTES=ENV["ACCESS_TOKEN_EXPIRE_MINUTES"]
URL_CHAT=ENV["URL_CHAT"]
ENTITY_UUID=ENV["ENTITY_UUID"]

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)



def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(db: Session, data: dict, expires_delta: Union[timedelta, None] = None):
    user_data = db.query(User).filter(User.username == data['username']).first()
    data_to_encode = {
        "sub": data['sub'],
        "username": user_data.username,
        "email": user_data.email,
        "name": user_data.name,
        "phone": user_data.phone,
        "verified": user_data.verified,
        "uuid": user_data.uuid
    }
    to_encode = data_to_encode.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    token = Token(
        access_token=encoded_jwt,
        token_type="Bearer",
        user_id=int(to_encode['sub'])
    )
    past_token = db.query(Token).filter(Token.user_id == int(to_encode['sub'])).first()
    if past_token:
        db.delete(past_token)
    db.add(token)
    db.commit()
    db.refresh(token)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(f"get_current_user(): token = {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        print(f"get_current_user(): username = {username}")

        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(
            user_id=int(user_id),
            username=username,
            email=payload.get("email"),
            name=payload.get("name"),
            phone=payload.get("phone"),
            verified=payload.get("verified"),
            uuid=payload.get("uuid")
        )

    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    correct_token = db.query(Token).filter(Token.user_id == int(user_id)).first()
    if token != correct_token.access_token:
        raise credentials_exception
    return user

def create_user(db: Session, user: schemas.UserCreate):
    if not(utils.verify_email(user.email)):
        raise HTTPException(status_code=400, detail="Invalid email")
    password_hash = get_password_hash(user.hashed_password)
    db_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        phone=user.phone,
        hashed_password=password_hash,
        uuid=uuid.uuid4()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_verification_email(db: Session, user_id: int, token: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.verified == True:
        raise HTTPException(status_code=400, detail="User already verified")
    verification_email = db.query(VerificationEmail).filter(VerificationEmail.user_id == user_id).first()
    if verification_email != None:
        return verification_email
    verification_email = VerificationEmail(user_id=user_id, access_token=token)
    db.add(verification_email)
    db.commit()
    db.refresh(verification_email)
    return verification_email


def get_verification_email(db: Session, user_id: int, token: str):
    VerEmail = db.query(VerificationEmail).filter(VerificationEmail.user_id == user_id).first()
    email_token = VerEmail.access_token
    return db.query(VerificationEmail
        ).filter(VerificationEmail.user_id == user_id, VerificationEmail.access_token == token).first()


def create_chat_token(user: schemas.User, sender_id: int, db: Session):
    data_to_encode = {
        "exp": 1738285323,
        "sub": user.uuid,
        "entityUUID": ENTITY_UUID,
        "userUUID": user.uuid,
        "levelOnEntity": 100
    }
    to_encode = data_to_encode.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    other_user = db.query(User).filter(User.id == sender_id).first()
    return {"token": encoded_jwt, "other_user_uuid": other_user.uuid}