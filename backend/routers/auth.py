from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Union
import requests
from db.models import ENV, Session, get_db
from db import schemas, crud
from dependencies import utils
import json

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=schemas.TokenBase)
async def login_user(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    try: 
        data = {
            "username": user_data.username,
            "password": user_data.password
        }
        data = json.dumps(data, indent = 4)
        headers = {"Content-Type": "application/json"}
        proxies = {"http": ENV['URL_AUTH']}
        request_session = requests.post(ENV['URL_AUTH']+"/auth/login", data=data, headers=headers, proxies=proxies)
        response_token = request_session.json()
        return response_token
        # return schemas.TokenBase(
        #     access_token = response["access_token"],
        #     token_type = response["token_type"]
        # )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/verify")
async def verify_auth(request: Request):
    try:
        token = request.headers.get('Authorization')
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        proxies = {"http": ENV['URL_AUTH']}
        request_session = requests.get(ENV['URL_AUTH']+"/auth/verify", headers=headers, proxies=proxies)
        response = request_session.json()
        print(response)
        if request:
            print("Correct token")
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
            headers={"WWW-Authenticate": "Bearer"},
        )
