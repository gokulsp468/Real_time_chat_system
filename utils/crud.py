from sqlalchemy.orm import Session
from app.models import Message


async def save_message(db: Session, room_id: str, sender: str, content: str):
    """Store a message in the database."""
    new_message = Message(room_id=room_id, sender=sender, content=content)
    db.add(new_message)
    db.commit()

async def get_previous_messages(db: Session, room_id: str, limit: int = 50):
    """Retrieve the last N messages for a room."""
    return db.query(Message).filter(Message.room_id == room_id).order_by(Message.timestamp.desc()).limit(limit).all()