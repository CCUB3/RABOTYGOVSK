from contextlib import asynccontextmanager

from fastapi import FastAPI
from pygments.lexers import web

from database import create_db_and_tables
from routes import websocket, messages, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # runs on startup
    yield

if __name__ == "__main__":
    app = FastAPI()
    app.include_router(messages.router)
    app.include_router(users.router)
    app.include_router(websocket.router)
