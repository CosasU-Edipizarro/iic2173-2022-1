from fastapi import APIRouter, Depends, HTTPException
from db.models import ENV, Session, get_db
from db import schemas, crud
from dependencies import utils


router = APIRouter(prefix="/users")


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.User:
    user = crud.get_user_by_email(db, email=user.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.get_user_by_username(db, username=user.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user=user)


@router.get("/", response_model=list[schemas.User])
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
) -> list[schemas.User]:
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/locations", response_model=schemas.Location)
async def create_location_for_user(
    user_id: int, 
    location: schemas.LocationCreate, 
    db: Session = Depends(get_db)
) -> schemas.Location:
    return crud.create_user_location(db=db, user_id=user_id, location=location)


@router.get("/{user_id}/locations", response_model=list[schemas.Location])
async def read_locations_for_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[schemas.Location]:
    return crud.get_user_locations(db=db, user_id=user_id, skip=skip, limit=limit)

@router.get("/{user_id}/locations/{location_id}", response_model=schemas.Location)
async def read_location_for_user(
    user_id: int,
    location_id: int,
    db: Session = Depends(get_db)
) -> schemas.Location:
    return crud.get_user_location(db=db, user_id=user_id, location_id=location_id)
