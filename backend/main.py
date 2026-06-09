from contextlib import asynccontextmanager

from fastapi import FastAPI
from pygments.lexers import web
import models

from database import create_db_and_tables
from routes import websocket, messages, users, token


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # runs on startup
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(messages.router)
app.include_router(users.router)
app.include_router(websocket.router)
app.include_router(token.router)