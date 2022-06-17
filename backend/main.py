from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.db_migration import db_migration
from db.populate import db_populate
from routers import routers
from tasks.celery_utils import create_celery


def create_app() -> FastAPI:

    db_migration()
    db_populate()

    current_app = FastAPI(title="IIC2173", version="1.0.0", )

    current_app.celery_app = create_celery()

    current_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    current_app.include_router(routers["auth"])
    current_app.include_router(routers["users"])
    current_app.include_router(routers["pings"])
    current_app.include_router(routers["locations"])
    current_app.include_router(routers["protected"])
    current_app.include_router(routers["count"])
    current_app.include_router(routers["externalapi"])


    @current_app.get("/")
    def read_root():
        return {"Hello": "World of FastAPI G19"}

    return current_app


app = create_app()
celery = app.celery_app





# # curl http://localhost:8888/tasks -H "Content-Type: application/json" --data '{"type": 0}'
# from dependencies.tasks import hello, create_task

# # def run_task(payload = Body(...)):
# @app.get("/tasks", status_code=201)
# def run_task():
#     # task_type = payload["type"]
#     print("Entrando a task endpoint")
#     # return {"Hello": "World of FastAPI G19"}
#     task = create_task.delay()
#     return { "task": "created" }
