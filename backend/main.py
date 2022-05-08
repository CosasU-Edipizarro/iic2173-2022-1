from db.db_migration import db_migration
from fastapi import FastAPI
from routers import routers

db_migration()

app = FastAPI()


app.include_router(routers["auth"])
app.include_router(routers["users"])
app.include_router(routers["locations"])
app.include_router(routers["protected"])
app.include_router(routers["emails"])

@app.get("/")
async def read_root():
    return {"Hello": "World of FastAPI G19"}
