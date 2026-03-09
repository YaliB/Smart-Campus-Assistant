from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ==========================================
# FAQ Schemas
# ==========================================
class FAQCreate(BaseModel):
    question: str
    answer: str
    tags: Optional[str] = None

class FAQResponse(FAQCreate):
    id: int

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    tags: Optional[str] = None

# ==========================================
# Room Schemas
# ==========================================
class RoomCreate(BaseModel):
    room_name: str
    building: str
    description: Optional[str] = None

class RoomResponse(RoomCreate):
    id: int

    class Config:
        from_attributes = True

class RoomUpdate(BaseModel):
    room_name: Optional[str] = None
    building: Optional[str] = None
    description: Optional[str] = None

# ==========================================
# Exam Schedule Schemas
# ==========================================
class ExamScheduleCreate(BaseModel):
    course_name: str
    exam_date: datetime
    location: str

class ExamScheduleResponse(ExamScheduleCreate):
    id: int

    class Config:
        from_attributes = True

class ExamScheduleUpdate(BaseModel):
    course_name: Optional[str] = None
    exam_date: Optional[datetime] = None
    location: Optional[str] = None

# ==========================================
# Reception Hour Schemas
# ==========================================
class ReceptionHourCreate(BaseModel):
    department: str
    hours: str
    contact_info: Optional[str] = None

class ReceptionHourResponse(ReceptionHourCreate):
    id: int

    class Config:
        from_attributes = True

class ReceptionHourUpdate(BaseModel):
    department: Optional[str] = None
    hours: Optional[str] = None
    contact_info: Optional[str] = None