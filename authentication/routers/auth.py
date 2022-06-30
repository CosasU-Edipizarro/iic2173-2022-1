from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from db.models import ENV, Session, get_db
from db import schemas, crud
from dependencies import utils


router = APIRouter(prefix="/auth")

@router.post("/login", response_model=schemas.TokenBase)
async def login_for_access_token(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        db=db, data={"sub": str(user.id), "username": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/verify", response_model=schemas.User)
async def verify_auth(current_user: schemas.User = Depends(crud.get_current_user)):
    print(current_user)
    return current_user