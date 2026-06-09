from starlette.websockets import WebSocket

from database import SessionDep
from models import MessageDB


async def create_message(owner: str, text: str, session: SessionDep):
    messagedb = MessageDB(text=text, owner=owner)
    session.add(messagedb)
    session.commit()
    session.refresh(messagedb)
    return messagedb

class WebSocketManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, ws: WebSocket):
        await ws.accept()
        self.connections.update({user_id: ws})

    def disconnect(self, user_id: str):
        self.connections.pop(user_id)

    async def send(self, message: dict, session: SessionDep):
        await create_message(owner=message.get("owner"), text=message.get("text"), session=session)
        for user_id in self.connections.keys():
            ws = self.connections.get(user_id)
            if ws:
                await ws.send_json(message)