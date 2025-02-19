from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from utils.auth_helper import get_current_user_from_websocket
from utils.crud import save_message, get_previous_messages
from app.database import get_db
from sqlalchemy.orm import Session


# router = APIRouter()
# active_connections = {}

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)


# manager = ConnectionManager()

# @router.websocket("/ws/{room_id}")
# async def websocket_endpoint(websocket: WebSocket, room_id: str,  db: Session = Depends(get_db)):
    
#     user = await get_current_user_from_websocket(websocket)
#     await websocket.accept()

#     if room_id not in active_connections:
#         active_connections[room_id] = []
#     active_connections[room_id].append(websocket)

    
#     previous_messages = await get_previous_messages(db, room_id)
#     for msg in reversed(previous_messages):  # Send in correct order
#         await websocket.send_text(f"{msg.sender}: {msg.content}")

#     try:
#         while True:
#             message = await websocket.receive_text()

            
#             await save_message(db, room_id, user, message)

            
#             for connection in active_connections[room_id]:
#                 await connection.send_text(f"{user}: {message}")

#     except WebSocketDisconnect:
#         active_connections[room_id].remove(websocket)





router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]  # Cleanup empty room

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, room_id: str, message: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, db: Session = Depends(get_db)):
    user = await get_current_user_from_websocket(websocket)
    await manager.connect(room_id, websocket)
    
    # Send previous messages
    previous_messages = await get_previous_messages(db, room_id)
    for msg in reversed(previous_messages):
        await websocket.send_text(f"{msg.sender}: {msg.content}")

    try:
        while True:
            message = await websocket.receive_text()
            await save_message(db, room_id, user, message)
            await manager.broadcast(room_id, f"{user}: {message}")
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        await manager.broadcast(room_id, f"{user} left the chat")
