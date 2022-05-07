from fastapi import APIRouter, Depends, HTTPException
from db.models import ENV, Session, get_db
from db import schemas, crud
from dependencies import utils


router = APIRouter(prefix="/locations")

@router.get("/", response_model=list[schemas.Location])
async def read_locations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[schemas.Location]:
    return crud.get_locations(db, skip=skip, limit=limit)
