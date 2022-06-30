from fastapi import FastAPI, Depends
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from db.db_migration import db_migration
from db.crud import oauth2_scheme, get_current_user
from db.models import Session, get_db
from routers import routers
from routers.auth import verify_auth
from fastapi.security import OAuth2PasswordBearer


db_migration()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routers["auth"])
app.include_router(routers["users"])
app.include_router(routers["chat"])


@app.get("/")
async def read_root(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    print(token)
    # Verify token
    current_user = await get_current_user(db, token)
    print(current_user)
    # if not verified raise error unathorized
    if await verify_auth():
        return {"Hello": "World of FastAPI Auth service"}