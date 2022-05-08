from fastapi import HTTPException

from db.models import Session, User, JWT, Location, Ping, VerificationEmail
from db import schemas
from dependencies import utils


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    if not(utils.verify_email(user.email)):
        raise HTTPException(status_code=400, detail="Invalid email")
    password_hash = utils.generate_password_hash(user.password)
    db_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        phone=user.phone,
        instagram=user.instagram,
        sex=user.sex,
        password=password_hash,
        verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Location).offset(skip).limit(limit).all()


def get_user_locations(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Location).filter(Location.user_id == user_id).offset(skip).limit(limit).all()


def create_user_location(db: Session, user_id: int, location: schemas.LocationCreate):
    new_location = Location(**location.dict(), user_id=user_id)
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location


def get_user_location(db: Session, user_id: int, location_id: int):
    return db.query(Location).filter(Location.user_id == user_id, Location.id == location_id).first()


def create_jwt(db: Session, user_id: int):
    token = utils.generate_unique("hex")
    jwt = JWT(
        user_id=user_id,
        token=token
    )
    db.add(jwt)
    db.commit()
    db.refresh(jwt)
    return jwt


def get_jwt(db: Session, user_id: int, user_password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    if utils.verify_password_hash(user_password, user.password):
        if user.jwt != None: # Delete old jwt
            db.query(JWT).filter(JWT.user_id == user.id).delete()
            db.commit()
        jwt = create_jwt(db, user.id)
        jwt = db.query(JWT).filter(JWT.user_id == user_id).first()
        jwt = JWT(user_id=user_id) if jwt is None else jwt
        db.add(jwt)
        return jwt
    else:
        raise HTTPException(status_code=401, detail="Wrong password")


def get_user_pings_received(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    pings = db.query(Ping).filter(Ping.receiver_id == user_id).offset(skip).limit(limit).all()
    return pings


def get_user_pings_sent(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    pings = db.query(Ping).filter(Ping.sender_id == user_id).offset(skip).limit(limit).all()
    return pings


def create_ping(db: Session, sender_id: int, receiver_id: int):
    ping = Ping(sender_id = sender_id, receiver_id = receiver_id)
    db.add(ping)
    db.commit()
    db.refresh(ping)
    return ping


def create_verification_email(db: Session, user_id: int):
    token = utils.generate_unique("hex")
    user = db.query(User).filter(User.id == user_id).first()
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.verified == False:
        raise HTTPException(status_code=400, detail="User already verified")
    verification_email = db.query(VerificationEmail).filter(VerificationEmail.user_id == user_id).first()
    if verification_email != None:
        return verification_email
    verification_email = VerificationEmail(user_id = user_id, token = token)
    db.add(verification_email)
    db.commit()
    db.refresh(verification_email)
    return verification_email
