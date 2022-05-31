import datetime
from fastapi import HTTPException

from db.models import Session, User, Location, Ping
from db import schemas
from routers.users import read_users
from dependencies import utils
from jose import JWTError, jwt


SECRET_KEY = "b75f0e58f700478526706d771021c3a057fa9118d2c0166adb05e00cb55b93c2"
ALGORITHM = "HS256"

def jwt_decode(token):
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

def get_user_by_token(db: Session, token: str):
    token = token.split(" ")[1]
    print(token)
    data = jwt_decode(token)
    print("FIN DE DECODING")
    user = get_user_by_auth_id(db, int(data['sub']))
    data['user_id'] = user.id
    return data


  
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_auth_id(db: Session, auth_id: int):
    return db.query(User).filter(User.auth_id == auth_id).first()

  
def get_user_by_token(db: Session, token: str):
    data = jwt_decode(token)
    print("FIN DE DECODING")
    user_id = int(data['sub'])
    print(data)
    print(user_id)
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, auth_id: int):
    db_user = User(
        auth_id = auth_id
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
    coordinates = f"{location.coords.split(',')[1].replace(' ', '')} {location.coords.split(',')[0].replace(' ', '')}"
    coordinates = f"SRID=4326;POINT({coordinates})"
    location.coords = coordinates
    new_location = Location(**location.dict(), user_id=user_id)
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location


def get_user_location(db: Session, user_id: int, location_id: int):
    return db.query(Location).filter(Location.user_id == user_id, Location.id == location_id).first()


# def create_jwt(db: Session, user_id: int):
#     token = utils.generate_unique("hex")
#     jwt = JWT(
#         user_id=user_id,
#         token=token
#     )
#     db.add(jwt)
#     db.commit()
#     db.refresh(jwt)
#     return jwt


# def get_jwt(db: Session, user_id: int, user_password: str):
#     user = db.query(User).filter(User.id == user_id).first()
#     if user == None:
#         raise HTTPException(status_code=404, detail="User not found")
#     if utils.verify_password_hash(user_password, user.password):
#         if user.jwt != None: # Delete old jwt
#             db.query(JWT).filter(JWT.user_id == user.id).delete()
#             db.commit()
#         jwt = create_jwt(db, user.id)
#         jwt = db.query(JWT).filter(JWT.user_id == user_id).first()
#         jwt = JWT(user_id=user_id) if jwt is None else jwt
#         db.add(jwt)
#         return jwt
#     else:
#         raise HTTPException(status_code=401, detail="Wrong password")


# def get_jwt_by_username(db: Session, user_username: str, user_password: str):
#     user = db.query(User).filter(User.username == user_username).first()
#     if user == None:
#         raise HTTPException(status_code=404, detail="User not found")
#     if utils.verify_password_hash(user_password, user.password):
#         if user.jwt != None: # Delete old jwt
#             db.query(JWT).filter(JWT.user_id == user.id).delete()
#             db.commit()
#         jwt = create_jwt(db, user.id)
#         return jwt
#     else:
#         raise HTTPException(status_code=401, detail="Wrong password")



async def get_user_pings_received(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    pings = db.query(Ping).filter(Ping.receiver_id == user_id).offset(skip).limit(limit).all()
    all_users = await read_users(db=db)
    senders = {}
    for ping in pings:
        for user in all_users:
            if user["user_id"] == ping.sender_id:
                senders[ping.sender_id] = user
                (senders[ping.sender_id]).update({
                    "sidi": ping.sidi,
                    "siin": ping.siin,
                    "dindin": ping.dindin
                })
    return senders


async def get_user_pings_sent(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    pings = db.query(Ping).filter(Ping.sender_id == user_id).offset(skip).limit(limit).all()
    all_users = await read_users(db=db)
    receivers = {}
    for ping in pings:
        for user in all_users:
            if user["user_id"] == ping.receiver_id:
                receivers[ping.receiver_id] = user
                (receivers[ping.receiver_id]).update({
                    "sidi": ping.sidi,
                    "siin": ping.siin,
                    "dindin": ping.dindin
                })
    return receivers


def create_ping(db: Session, sender_id: int, receiver_id: int, siin: float, sidi: float, dindin: float):
    ping = Ping(sender_id = sender_id, receiver_id = receiver_id, siin = siin, sidi = sidi, dindin = dindin)
    db.add(ping)
    db.commit()
    db.refresh(ping)
    return ping


