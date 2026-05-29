
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from RABOTYGOVSK.backend.database import SessionDep
from RABOTYGOVSK.backend.models.user import UserIn, UserRegister, UserDB, UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get('/', response_model=list[UserOut])
async def get_users(session: SessionDep):
    users = session.exec(select(UserDB)).all()
    return users

@router.put('/', response_model=UserOut)
async def create_user(user: UserRegister, session: SessionDep):
    db_user = UserDB.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get('/{user_id}', response_model=UserOut)
async def get_user_by_id(user_id: int, session: SessionDep):
    user = session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
