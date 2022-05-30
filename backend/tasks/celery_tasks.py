from typing import List
import time
from celery import shared_task
from db import crud
from db.models import ENV, get_db, Location
from geoalchemy2 import functions
from sqlalchemy import func
from routers.users import read_locations_for_user
from math import log


@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name="hello_world:celery_hello_world")
def celery_hello_world(self):
    print("Hello World from Celery")
    time.sleep(5)
    return True

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name="hello_world:celery_sidi")
async def sidi(self,user_id1,user_id2):#id de los user
    db = get_db() # new Session()
    centroid1, total1 = db.query(functions.ST_Centroid(Location.coords), func.count(Location)).filter(Location.user_id == user_id1).offset(0).limit(100).all()
    print('primera query lista')
    centroid2, total2 = db.query(functions.ST_Centroid(Location.coords), func.count(Location)).filter(Location.user_id == user_id2).offset(0).limit(100).all()
    print('segunda query lista')
    print(centroid1,centroid2,total1,total2, sep='\n')    
    length = functions.ST_Distance(centroid1, centroid2)
    print('distancia calculada', length)
    
    return (total1+total2)/log(length)

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name="hello_world:celery_siin")
async def siin(self,user_id1,user_id2):#id o el user
    tags = ['Entretención', 'Deporte', 'Arte', 'Historia', 'Música', 'Comida', 'Animales', 'Eventos', 'Académico', 'Familia']
    count_1= await count_places(user_id1)
    count_2= await count_places(user_id2)
    diff = 0
    total = 0
    for tag in tags:
        p1 = count_1.get(tag, 0)
        p2 = count_2.get(tag, 0)
        diff += abs(p1-p2)
        total+=p1+p2
    print('DENTRO DE SIIN TERMINADO!!!!!!!!!!!!!')
    return (total-diff)/(total)

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name="hello_world:celery_count_places")
async def count_places(self,uid):
    places = await read_locations_for_user(uid)
    count = {}
    for place in places:
        count[place.tag] = count.get(place.tag, 0) + 1
    return count


@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name="hello_world:celery_dindin")
async def dindin(self,uid1,uid2):
    print('EMPEZANDO A CALCULAR DIIN!!!!!!!!!!!!!!!')
    sidi_id = await sidi(uid1,uid2)
    print('SIDI_ID CALCULADOOOOOOOOOOOOOOOOOO', sidi_id)
    siin_id = await siin(uid1,uid2)
    print('SIIN_ID CALCULADOOOOOOOOOOOOOOOOOO', siin_id)

    return siin_id*sidi_id

# from api import universities


# @shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
#              name='universities:get_all_universities_task')
# def get_all_universities_task(self, countries: List[str]):
#     data: dict = {}
#     for cnt in countries:
#         data.update(universities.get_all_universities_for_country(cnt))
#     return data


# @shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
#              name='university:get_university_task')
# def get_university_task(self, country: str):
#     university = universities.get_all_universities_for_country(country)
#     return university