from fastapi import APIRouter, Depends, HTTPException, Request, Header, Request
from db.models import ENV, Session, get_db, User
from db import schemas, crud
from dependencies import utils
from routers.auth import verify_auth
from tasks.celery_tasks import celery_hello_world as celery_hello_world_celery

router = APIRouter( prefix="/protected" )


@router.get("/task")
def celery_hello_world() -> dict:
    print("Hello World")
    celery_hello_world_celery.delay()
    return {"Hello": "World of FastAPI G19"}

@router.get("/")
async def get_protected(request: Request, db: Session = Depends(get_db)):
    verify_auth(request)
    # print(user)
    return {"status": "ok"}