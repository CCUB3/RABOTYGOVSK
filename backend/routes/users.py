from datetime import timedelta
from pickletools import dis
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from starlette import status

from database import SessionDep
from models.token import Token
from models.user import UserIn, UserRegister, UserDB, UserOut
from services import auth
from services.auth import authenticate_user, get_current_active_user
from services.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(prefix="/users", tags=["users"])

@router.get('/', response_model=list[UserOut])
async def get_users(session: SessionDep):
    users = session.exec(select(UserDB)).all()
    return users

@router.put('/', response_model=UserOut)
async def create_user(user: UserRegister, session: SessionDep):
    username_taken = session.exec(select(UserDB).where(UserDB.username == user.username)).one_or_none()
    if username_taken:
        raise HTTPException(status_code=400, detail="Username taken")
    db_user = UserDB(username=user.username,
                     display_name=user.display_name,
                     hashed_password=auth.hash_password(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get('/me', response_model=UserOut)
async def get_me(current_user: Annotated[UserOut, Depends(get_current_active_user)]):
    return current_user


@router.get('/{user_id}', response_model=UserOut)
async def get_user_by_id(user_id: int, session: SessionDep):
    user = session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")