from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Room

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/create/")
def create_room(name: str, db: Session = Depends(get_db)):
    room = Room(name=name)
    db.add(room)
    db.commit()
    db.refresh(room)
    return {"room_id": room.id, "name": room.name}

@router.get("/list/")
def list_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()
