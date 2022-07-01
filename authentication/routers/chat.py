from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from db.models import ENV, Session, get_db
from db import schemas, crud
from dependencies import utils
from db.crud import get_current_user


router = APIRouter(prefix="/chat")

@router.get("/token/{sender_id}", response_model=schemas.ChatToken)
async def send_token_for_chat(
    sender_id: int, 
    current_user: schemas.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
    ):
    chat_token = crud.create_chat_token(current_user, sender_id, db)
    return chat_token