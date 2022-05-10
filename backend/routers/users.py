from gzip import READ
from fastapi import APIRouter, Depends, HTTPException
from db.models import ENV, Session, get_db, User, Location
from db import schemas, crud
from dependencies import utils
from geoalchemy2 import functions
from sqlalchemy import func

router = APIRouter(prefix="/users")


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    found_user = crud.get_user_by_email(db, email=user.email)
    if found_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    found_user = crud.get_user_by_username(db, username=user.username)
    if found_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_creado= crud.create_user(db=db, user=user)
    verification_email = crud.create_verification_email(db,user_creado.id)
    await utils.send_verification_email(db, user_creado.id, user_creado.email,verification_email.token)
    await utils.send_verification_email(db, user_creado.id, 'ignacio.pasten2@gmail.com', verification_email.token)       
    return user_creado

@router.get("/{user_id}/verify/{token}")
def confirm_verification(user_id: int, token: str, db: Session = Depends(get_db)) -> dict:
    print("confirm_verification")
    vertification_email = crud.get_verification_email(db, user_id, token)
    if not vertification_email:
        raise HTTPException(status_code=400, detail="Invalid token")
    vertification_email.verified = True
    db.commit()
    return {"status": "ok"}

@router.get("/", response_model=list[schemas.User])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
) -> list[schemas.User]:
    print("ENTRANDO A /USERS")
    users = crud.get_users(db, skip=skip, limit=limit)
    print(users)
    return users


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/locations", response_model=schemas.Location)
async def create_location_for_user(
    location: schemas.LocationCreate,
    user: User = Depends(utils.get_user_by_token), 
    db: Session = Depends(get_db)
):
    temp = crud.create_user_location(db=db, user_id=user.id, location=location)
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
