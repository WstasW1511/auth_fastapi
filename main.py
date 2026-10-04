from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.core.config import *
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.database import AsyncSessionLocal
from app.db.init_db import init_roles



@asynccontextmanager
async def lifespan(app: FastAPI):

    async with AsyncSessionLocal() as db:
        await init_roles(db)

    yield


app = FastAPI(title='Auth', lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(users_router)

