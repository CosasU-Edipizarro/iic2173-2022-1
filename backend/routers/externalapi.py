from fastapi import APIRouter, Depends, HTTPException, Request, Header
from db.models import ENV, Session, get_db, User
from db import schemas, crud
from dependencies import utils
import requests

router = APIRouter( prefix="/externalapi" )

@router.get("/getstreet/{latlong}")
async def get_street(latlong: str):
    API_URL = f"http://api.positionstack.com/v1/reverse?access_key={ENV['GEOLOCATION_API_KEY']}&query={latlong}"
    r = requests.get(API_URL)
    data = r.json()
    parsed_data = {
        "address": f"{data['data'][0]['street']}, {data['data'][0]['number']}, {data['data'][0]['region']}, {data['data'][0]['country']}"
    }
    return {
        "status": "ok",
        "data": parsed_data
    }