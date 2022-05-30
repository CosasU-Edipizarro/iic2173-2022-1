import os
from gzip import READ
from fastapi import APIRouter, Depends, HTTPException, Request
from db.models import ENV, Session, get_db, User, Location
from db import schemas, crud
from dependencies import utils
from geoalchemy2 import functions
from sqlalchemy import func
import json 

import requests

router = APIRouter(prefix="/users")


@router.post("/", response_model=schemas.TokenBase)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        print("POST /users/")
        print(user)
        data = {
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "hashed_password": user.hashed_password
        }

        data = json.dumps(data, indent = 4)
        headers = {"Content-Type": "application/json"}
        proxies = { "http": ENV['URL_AUTH'] }
        request_session = requests.post(ENV['URL_AUTH']+"/users", data=data, headers=headers, proxies=proxies)
        response_token = request_session.json()
        
        jwt_data = crud.jwt_decode(response_token["access_token"])
        print(jwt_data)

        found_user = crud.get_user_by_auth_id(db, auth_id=int(jwt_data["sub"]))
        if found_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_creado = crud.create_user(db=db, auth_id=int(jwt_data["sub"]))

        return response_token
    except Exception as exception:
        print("Error en POST /users/")
        print(exception)
        raise HTTPException(status_code=400, detail="An error has ocurred")

@router.get("/", response_model=list[schemas.User])
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
) -> list[schemas.User]:
    print("ENTRANDO A /users")
    print(f"URL TO GET DATA: {ENV['URL_AUTH']+'/users'}")

    headers={'Content-Type': 'application/json'}
    proxies = { "http": ENV['URL_AUTH'] }
    request_session = requests.get(ENV['URL_AUTH']+"/users", headers=headers, proxies=proxies)
    print("GET /users/: Justo después del request")

    users = request_session.json()

    # users = crud.get_users(db, skip=skip, limit=limit)
    print(users)
    return users


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/user", response_model=schemas.User)
async def read_user_from_jwt(request: Request, db: Session = Depends(get_db)) -> schemas.User:
    token = request.headers.get('Authorization')
    print(token)
    print("ENTRANDO A GET USER BY TOKEN")
    db_user = crud.get_user_by_token(db, token)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/locations", response_model=schemas.Location)
async def create_location_for_user(
    user_id: int,
    location: schemas.LocationCreate, 
    db: Session = Depends(get_db)
):
    temp = crud.create_user_location(db=db, user_id=user_id, location=location)
    # temp.coords = f"{func.st_y(temp.coords)}, {func.st_x(temp.coords)}"
    temp.coords = str(functions.ST_AsText(temp.coords))
    return temp


@router.get("/{user_id}/locations", response_model=list[schemas.Location])
async def read_locations_for_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[schemas.Location]:
    locations = crud.get_user_locations(db=db, user_id=user_id, skip=skip, limit=limit)
    new_locations = []
    for location in locations:
        query_location = db.query(
            Location, 
            func.st_y(Location.coords), 
            func.st_x(Location.coords)
        ).filter(Location.id == location.id).first()
        location.coords = f"{query_location[1]}, {query_location[2]}"
        new_locations.append(location)

    return new_locations


@router.get("/{user_id}/locations/{location_id}", response_model=schemas.Location)
async def read_location_for_user(
    user_id: int,
    location_id: int,
    db: Session = Depends(get_db)
) -> schemas.Location:
    return crud.get_user_location(db=db, user_id=user_id, location_id=location_id)
