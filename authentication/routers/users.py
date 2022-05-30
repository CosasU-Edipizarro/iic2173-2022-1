from gzip import READ
from os import access
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from db.models import ENV, Session, get_db, User
from db import schemas, crud
from dependencies import utils
from geoalchemy2 import functions
from sqlalchemy import func
from routers import auth

router = APIRouter(prefix="/users")


@router.post("/", response_model=schemas.TokenBase)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print("POST /users/ de auth")
    print(user)
    found_user = crud.get_user_by_email(db, email=user.email)
    if found_user:
        print("USER FOUND")
        raise HTTPException(status_code=400, detail="Email already registered")
    found_user = crud.get_user_by_username(db, username=user.username)
    if found_user:
        print("USER FOUND")
        raise HTTPException(status_code=400, detail="Username already registered")
    print("BEFORE CREATE USER")
    created_user = crud.create_user(db=db, user=user)
    print("AFTER CREATE USER")

    token = await auth.login_for_access_token(db=db, user_data=schemas.UserLogin(username=user.username, password= user.hashed_password))
    access_token = token['access_token']

    verification_email = crud.create_verification_email(db, created_user.id, str(access_token))
    await utils.send_verification_email(db, created_user.id, created_user.email, verification_email.access_token)
    await utils.send_verification_email(db, created_user.id, 'ignacio.pasten2@gmail.com', verification_email.access_token)       
    return token

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
    print("ENTRANDO A auth/users")
    users = crud.get_users(db, skip=skip, limit=limit)
    print(users)
    return users

#borrar si es que
@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user