from fastapi import APIRouter, Depends, HTTPException, Request
from db.models import ENV, Session, get_db, User, Ping
from db import schemas, crud

from dependencies import utils
from tasks.celery_tasks import dindin


router = APIRouter(prefix="/pings")

@router.post("/{sender_id}/{receiver_id}", response_model=schemas.Ping)
async def create_user_ping(
    sender_id: int,
    receiver_id: int,
    db: Session = Depends(get_db)
):
    temp = crud.create_ping(db=db, sender_id=sender_id, receiver_id=receiver_id)
    index = await dindin(sender_id,receiver_id)
    print("din din indexxxxxxxx:", index)
    return temp


@router.get("/received/{user_id}", response_model=list[schemas.User])
def read_user_received_pings(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[schemas.User]:
    senders = crud.get_user_pings_received(db=db, user_id=user_id, skip=skip, limit=limit)
    return senders

@router.get("/sent/{user_id}", response_model=list[schemas.User])
def read_user_sent_pings(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[schemas.User]:
    receivers = crud.get_user_pings_sent(db=db, user_id=user_id, skip=skip, limit=limit)
    return receivers