from fastapi import APIRouter
from sqlalchemy import select

from database import SessionDep
from models.message import MessageOut, MessageDB

router = APIRouter(prefix="/messages")

@router.get("/", response_model=list[MessageOut])
async def get_messages(session: SessionDep):
    messages = session.exec(select(MessageDB)).all()
    return messages

@router.delete("/{message_id}/", response_model=MessageOut)
async def delete_message(session: SessionDep, message_id: int):
    message = session.get(MessageDB, message_id)
    session.delete(message)
    return message