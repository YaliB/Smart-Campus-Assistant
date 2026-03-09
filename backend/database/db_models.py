from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Base class for all SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # Determine if the user has admin privileges to edit campus info
    is_admin = Column(Boolean, default=False)

class ReceptionHour(Base):
    __tablename__ = "reception_hours"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True, nullable=False)
    hours = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)

class ExamSchedule(Base):
    __tablename__ = "exam_schedules"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, index=True, nullable=False)
    exam_date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String, index=True, nullable=False)
    building = Column(String, nullable=False)
    description = Column(Text, nullable=True)

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=False)
    tags = Column(String, nullable=True)