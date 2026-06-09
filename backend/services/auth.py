from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.util.queue import Queue
from sqlmodel import select
from starlette import status
from starlette.websockets import WebSocket

from database import SessionDep
from models.token import TokenData
from models.user import UserDB, UserOut
from services.token import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def authenticate_user(username: str, password: str, session: SessionDep):
    user = session.exec(select(UserDB).where(UserDB.username == username)).one_or_none()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = session.exec(select(UserDB).where(UserDB.username == token_data.username)).one()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserOut, Depends(get_current_user)],
):
    return current_user


async def get_current_websocket_user(websocket: WebSocket,
                                 session: SessionDep, token: str = Query(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            await websocket.close(code=4001)
            return None
        token_data = TokenData(username=username)
    except InvalidTokenError:
        await websocket.close(code=4001)
        return None

    user = session.exec(select(UserDB).where(UserDB.username == token_data.username)).one()
    if user is None:
        await websocket.close(code=4001)
        return None

    return user