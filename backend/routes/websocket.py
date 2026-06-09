from typing import Annotated

from fastapi import APIRouter, WebSocket, Depends, HTTPException, Cookie, Query, WebSocketException
from starlette import status
from starlette.websockets import WebSocketDisconnect

from database import SessionDep
from models.user import UserOut, UserDB
from services.auth import get_current_active_user, oauth2_scheme, get_current_websocket_user
from services.managers import WebSocketManager

router = APIRouter(prefix="/ws", tags=["websocket"])
wsmanager = WebSocketManager()

# @router.websocket("/{user_id}/")
# async def websocket_endpoint(user_id:int, websocket: WebSocket, session: SessionDep):
#     await wsmanager.connect(str(user_id), websocket)
#     try:
#         while True:
#             data = await websocket.receive_json()
#
#             message = {
#                 "owner": str(user_id),
#                 "text": data["text"]
#             }
#
#             await wsmanager.send(message, session)
#     except WebSocketDisconnect:
#         wsmanager.disconnect(str(user_id))



@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket, session: SessionDep, current_user: Annotated[UserDB, Depends(get_current_websocket_user)]):

    if not current_user:
        await websocket.close(code=4001)
        raise HTTPException(status_code=403)
    await wsmanager.connect(current_user.username, websocket)
    try:
        while True:
            data = await websocket.receive_json()

            message = {
                "owner": current_user.username,
                "text": data["text"]
            }

            await wsmanager.send(message, session)
    except WebSocketDisconnect:
        wsmanager.disconnect(current_user.username)