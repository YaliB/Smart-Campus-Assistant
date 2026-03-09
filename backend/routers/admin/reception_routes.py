from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database.db import get_db
from ...database.db_models import ReceptionHour
from ...api_models.knowledge_schemas import ReceptionHourCreate, ReceptionHourResponse, ReceptionHourUpdate

router = APIRouter()

@router.post("/", response_model=ReceptionHourResponse, status_code=status.HTTP_201_CREATED)
def create_reception_hour(reception: ReceptionHourCreate, db: Session = Depends(get_db)):
    """
    Create a new reception hour entry.
    """
    new_reception = ReceptionHour(
        department=reception.department,
        hours=reception.hours,
        contact_info=reception.contact_info
    )
    db.add(new_reception)
    db.commit()
    db.refresh(new_reception)
    return new_reception

@router.get("/", response_model=List[ReceptionHourResponse])
def get_all_reception_hours(db: Session = Depends(get_db)):
    """
    Retrieve all reception hours.
    """
    return db.query(ReceptionHour).all()

@router.delete("/{reception_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reception_hour(reception_id: int, db: Session = Depends(get_db)):
    """
    Delete a reception hour entry by its ID.
    """
    reception_to_delete = db.query(ReceptionHour).filter(ReceptionHour.id == reception_id).first()
    if not reception_to_delete:
        raise HTTPException(status_code=404, detail="Reception hour not found")
    
    db.delete(reception_to_delete)
    db.commit()
    return

@router.patch("/{reception_id}", response_model=ReceptionHourResponse)
def update_reception_hour(reception_id: int, reception_update: ReceptionHourUpdate, db: Session = Depends(get_db)):
    db_reception = db.query(ReceptionHour).filter(ReceptionHour.id == reception_id).first()
    if not db_reception:
        raise HTTPException(status_code=404, detail="Reception hour not found")
    
    update_data = reception_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_reception, key, value)
        
    db.commit()
    db.refresh(db_reception)
    return db_reception