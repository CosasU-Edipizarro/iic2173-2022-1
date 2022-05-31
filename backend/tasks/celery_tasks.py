from typing import List
import time
from celery import shared_task
from db import crud

from db.models import ENV, get_db, Location, Session, User
from geoalchemy2 import functions
from sqlalchemy import func
from routers.users import read_locations_for_user
from math import log, sqrt

from geoalchemy2 import Geometry, Geography



@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name="hello_world:celery_hello_world")
def celery_hello_world(self):
    print("Hello World from Celery")
    time.sleep(5)
    return True

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name="hello_world:celery_sidi")

def sidi(self,user_id1,user_id2):#id de los user
    print("sidi(): ")
    db = Session() # new Session() #db: Session = Depends(get_db)
    print(db)
    print('primera query lista')
    locations1= read_locations_for_user(user_id=user_id1, db=db)
    locations2= read_locations_for_user(user_id=user_id2, db=db)
    x_1, x_2, y_1, y_2, total = 0, 0, 0, 0, 0
    for place in locations1:
        place.coords = place.coords.split(',') # y , x
        x_1 +=float(place.coords[1])
        y_1 +=float(place.coords[0])
        total +=1
    for place in locations2:
        place.coords = place.coords.split(',') # y , x
        x_2 +=float(place.coords[1])
        y_2 +=float(place.coords[0])
        total +=1
    centroide_1 = (x_1/len(locations1), y_1/len(locations1))
    print("CENTROIDE 1: ", centroide_1)
    centroide_2 = (x_2/len(locations2), y_2/len(locations2))
    print("CENTROIDE 2: ", centroide_2)
    length = sqrt((centroide_1[0]-centroide_2[0])**2 + (centroide_1[1]-centroide_2[1])**2)
    print("DISTANCIA: ", length)    
    return (total)/log(length)

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name="hello_world:celery_siin")
def siin(self, user_id1, user_id2): #id o el user
    db = Session()
    tags = ['Entretención', 'Deporte', 'Arte', 'Historia', 'Música', 'Comida', 'Animales', 'Eventos', 'Académico', 'Familia']
    count_1, count_2= {}, {}
    places_1 = read_locations_for_user(user_id=user_id1, db=db)
    for place in places_1:
        count_1[place.tag] = count_1.get(place.tag, 0) + 1
    places_2 = read_locations_for_user(user_id=user_id2, db=db)
    for place in places_2:
        count_2[place.tag] = count_2.get(place.tag, 0) + 1

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
             name="hello_world:celery_dindin")
def dindin(self,uid1,uid2):
    print('EMPEZANDO A CALCULAR DIIN!!!!!!!!!!!!!!!')
    sidi_id = sidi(uid1,uid2)
    print('SIDI_ID CALCULADOOOOOOOOOOOOOOOOOO', sidi_id)
    siin_id = siin(uid1,uid2)
    print('SIIN_ID CALCULADOOOOOOOOOOOOOOOOOO', siin_id)

    data = {
        "siin": siin_id, 
        "sidi": sidi_id, 
        "dindin": siin_id*sidi_id
    }
    print(data)
    return data


