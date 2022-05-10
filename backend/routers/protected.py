from fastapi import APIRouter, Depends, HTTPException, Request, Header
from db.models import ENV, Session, get_db, JWT, User
from db import schemas, crud
from dependencies import utils

router = APIRouter( prefix="/protected" )

@router.get("/")
async def get_protected(db: Session = Depends(get_db), user: User = Depends(utils.get_user_by_token)):
    print(user)
    return {"status": "ok"}