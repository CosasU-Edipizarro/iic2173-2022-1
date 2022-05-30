from db.models import Session, ENV
from db.schemas import UserCreate
from db import crud
import requests

def create_users(db: Session):
    print("¡¡ create_users() !!")
    for i in range(1,13):
        data = {
            "name": f"User {i}",
            "username": f"user{i}",
            "email": f"user{i}@iic2171-g19.xyz",
            "phone": f"+56900000000{i}",
            "hashed_password": f"user{i}"
        }
        response = requests.post(ENV['URL_AUTH']+"/users", data = data)
        response = response.json()
        print(response)
        response = response[0]
        user_id = crud.jwt_decode(response)["sub"]
        crud.create_user(db=db, auth_id=int(user_id))
