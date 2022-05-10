from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.db_migration import db_migration
from db.populate import db_populate
from routers import routers


db_migration()
db_populate()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routers["auth"])
app.include_router(routers["users"])
app.include_router(routers["pings"])
app.include_router(routers["locations"])
app.include_router(routers["protected"])
app.include_router(routers["emails"])
app.include_router(routers["count"])
app.include_router(routers["externalapi"])


@app.get("/")
async def read_root():
    return {"Hello": "World of FastAPI G19"}
