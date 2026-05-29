from pydoc import text

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from RABOTYGOVSK.backend.database import SessionDep
from RABOTYGOVSK.backend.models.message import MessageDB

router = APIRouter(prefix="/ws", tags=["websocket"])

async def create_message(owner_id: int, text: str, session = SessionDep):
    messageDB = MessageDB(text=text, owner_id=owner_id)
    session.add(messageDB)
    session.commit()
    session.refresh(messageDB)
    return messageDB


class WebSocketManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, ws: WebSocket):
        await ws.accept()
        self.connections.update({user_id: ws})

    def disconnect(self, user_id: str):
        self.connections.pop(user_id)

    async def send(self, message: dict):
        await create_message(owner_id=int(message.get("owner")), text=message.get("text"))
        for user_id in self.connections.keys():
            ws = self.connections.get(user_id)
            if ws:
                await ws.send_json(message)

wsmanager = WebSocketManager()

@router.websocket("/{user_id}/")
async def websocket_endpoint(user_id:int, websocket: WebSocket):
    await wsmanager.connect(str(user_id), websocket)
    try:
        while True:
            data = await websocket.receive_json()

            message = {
                "owner": str(user_id),
                "text": data["text"]
            }

            await wsmanager.send(message)
    except WebSocketDisconnect:
        wsmanager.disconnect(str(user_id))
