from fastapi import APIRouter, Depends, HTTPException, Request
from db.models import ENV, Session, get_db, User, Ping
from db import schemas, crud

from dependencies import utils


router = APIRouter(prefix="/pings")

@router.post("/", response_model=schemas.Ping)
async def create_user_ping(
    request: Request,
    db: Session = Depends(get_db)
):
    data = await request.json()
    temp = crud.create_ping(db=db, sender_id=data.sender_id, receiver_id=data.receiver_id)
    return temp


@router.get("/{user_id}", response_model=list[schemas.Ping])
async def read_user_pings(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[schemas.Ping]:
    senders = await crud.get_user_pings_received(db=db, user_id=user_id, skip=skip, limit=limit)
    return senders