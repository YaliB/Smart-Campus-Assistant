from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database.db import get_db
from ...database.db_models import ExamSchedule
from ...api_models.knowledge_schemas import ExamScheduleCreate, ExamScheduleResponse, ExamScheduleUpdate

router = APIRouter()

@router.post("/", response_model=ExamScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_exam(exam: ExamScheduleCreate, db: Session = Depends(get_db)):
    """
    Create a new exam schedule entry.
    """
    new_exam = ExamSchedule(
        course_name=exam.course_name,
        exam_date=exam.exam_date,
        location=exam.location
    )
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    return new_exam

@router.get("/", response_model=List[ExamScheduleResponse])
def get_all_exams(db: Session = Depends(get_db)):
    """
    Retrieve all exam schedules.
    """
    return db.query(ExamSchedule).all()

@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    """
    Delete an exam schedule by its ID.
    """
    exam_to_delete = db.query(ExamSchedule).filter(ExamSchedule.id == exam_id).first()
    if not exam_to_delete:
        raise HTTPException(status_code=404, detail="Exam schedule not found")
    
    db.delete(exam_to_delete)
    db.commit()
    return

@router.patch("/{exam_id}", response_model=ExamScheduleResponse)
def update_exam(
    exam_id: int, 
    exam_update: ExamScheduleUpdate, 
    db: Session = Depends(get_db)
):
    """
    Partially update an existing exam schedule.
    Only the fields provided in the request body will be changed.
    """
    # 1. Fetch the existing exam from the database
    db_exam = db.query(ExamSchedule).filter(ExamSchedule.id == exam_id).first()
    
    if not db_exam:
        raise HTTPException(status_code=404, detail="Exam schedule not found")
    
    # 2. Extract only the fields that were explicitly set by the user
    # exclude_unset=True ensures we don't overwrite existing data with None
    update_data = exam_update.model_dump(exclude_unset=True)
    
    # 3. Dynamically update the attributes on the SQLAlchemy model
    for key, value in update_data.items():
        setattr(db_exam, key, value)
        
    # 4. Commit the changes and refresh the object
    db.commit()
    db.refresh(db_exam)
    
    return db_exam