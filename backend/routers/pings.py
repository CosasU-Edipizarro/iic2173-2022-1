from fastapi import APIRouter, Depends, HTTPException, Request, Response
from db.models import ENV, Session, get_db, User, Ping
from db import schemas, crud
from http import HTTPStatus

from dependencies import utils
from tasks.celery_tasks import dindin
from tasks.celery_utils import get_task_info


router = APIRouter(prefix="/pings")

@router.post("/", response_model=schemas.Ping)
async def create_user_ping(
    users: schemas.PingCreate,
    db: Session = Depends(get_db)
):
    sender_id = users.sender_id
    receiver_id = users.receiver_id
    print("create_user_ping")
    print(f"Sender id: {sender_id}")
    print(f"Receiver id: {receiver_id}")
    task = dindin.delay(sender_id, receiver_id)
    print("Task")
    print(task)
    print("Task Info")
    # print(get_task_info(task.id))
    index_data = dindin(sender_id, receiver_id)
    siin_data = index_data["siin"]
    sidi_data = index_data["sidi"]
    dindin_data = index_data["dindin"]
    temp = crud.create_ping(db=db, sender_id=sender_id, receiver_id=receiver_id, siin=siin_data, sidi=sidi_data, dindin=dindin_data)
    print("MODELLLLLLLLLLLLLLL:", temp)
    return temp


@router.get("/received/{user_id}")
async def read_user_received_pings(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    senders = await crud.get_user_pings_received(db=db, user_id=user_id, skip=skip, limit=limit)
    return senders

@router.get("/sent/{user_id}")
async def read_user_sent_pings(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    receivers = await crud.get_user_pings_sent(db=db, user_id=user_id, skip=skip, limit=limit)
    return receivers

@router.get("/accepted/{user_id}")
async def read_user_accepted_pings(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    friends = await crud.get_user_pings_accepted(db=db, user_id=user_id, skip=skip, limit=limit)
    return friends

@router.patch("/", response_model=schemas.Ping)
def accept_ping(
    users: schemas.PingBase,
    db: Session = Depends(get_db)
):
    return crud.accept_ping(db, users.sender_id, users.receiver_id)

@router.delete("/")
def deny_ping(
    users: schemas.PingBase,
    db: Session = Depends(get_db)
):
    crud.delete_ping(db, users.sender_id, users.receiver_id)
    return Response(status_code=HTTPStatus.NO_CONTENT.value)