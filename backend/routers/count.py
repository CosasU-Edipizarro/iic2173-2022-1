from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func

from db.models import ENV, Session, get_db, User
from db import schemas, crud
from dependencies import utils

router = APIRouter( prefix="/count" )

@router.get("/users", response_model=schemas.Count)
async def count_users(db: Session = Depends(get_db)) -> schemas.Count:
    count = db.query(func.count(User.id)).scalar()
    count = {"count": count}
    return count
