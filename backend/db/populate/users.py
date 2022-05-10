from db.models import Session
from db.schemas import UserCreate
from db import crud

def create_users(db: Session):
    print("¡¡ create_users() !!")
    for i in range(1,16):
        user = UserCreate(
            name=f"User {i}",
            username=f"user{i}",
            email=f"user{i}@iic2171-g19.xyz",
            phone=f"+56900000000{i}",
            password=f"user{i}"
        )
        crud.create_user(db=db, user=user)
