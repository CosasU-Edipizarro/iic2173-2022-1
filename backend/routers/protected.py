from fastapi import APIRouter, Depends, HTTPException
from db.models import ENV, Session, get_db
from db import schemas, crud
from dependencies import utils

router = APIRouter( prefix="/protected" )

@router.get("/")
async def get_protected(db: Session = Depends(get_db)):
    await utils.get_token_header(db=db)
    return {"status": "ok"}