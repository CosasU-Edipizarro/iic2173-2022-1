from fastapi import APIRouter, Depends, HTTPException
from db.models import ENV, Session, get_db
from db import schemas, crud
from dependencies import utils


router = APIRouter(prefix="/auth")


@router.post("/login", response_model=schemas.JWT)
async def create_jwt_for_user(
    user_id: int,
    user_password: str,
    db: Session = Depends(get_db)
) -> schemas.JWT:
    return crud.get_jwt(db=db, user_id=user_id, user_password=user_password)