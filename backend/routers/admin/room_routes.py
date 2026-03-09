from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database.db import get_db
from ...database.db_models import Room
from ...api_models.knowledge_schemas import RoomCreate, RoomResponse, RoomUpdate

router = APIRouter()

@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    """
    Create a new room entry.
    """
    new_room = Room(
        room_name=room.room_name,
        building=room.building,
        description=room.description
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.get("/", response_model=List[RoomResponse])
def get_all_rooms(db: Session = Depends(get_db)):
    """
    Retrieve all rooms.
    """
    return db.query(Room).all()

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """
    Delete a room by its ID.
    """
    room_to_delete = db.query(Room).filter(Room.id == room_id).first()
    if not room_to_delete:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db.delete(room_to_delete)
    db.commit()
    return

@router.patch("/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, room_update: RoomUpdate, db: Session = Depends(get_db)):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    update_data = room_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)
        
    db.commit()
    db.refresh(db_room)
    return db_room