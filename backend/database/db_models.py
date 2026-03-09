from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Base class for all SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # E.g., student ID
    student_id = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # Determine if the user has admin privileges to edit campus info
    is_admin = Column(Boolean, default=False)

class ReceptionHour(Base):
    __tablename__ = "reception_hours"

    id = Column(Integer, primary_key=True, index=True)
    # E.g., "Academic Secretariat", "IT Support"
    department = Column(String, index=True, nullable=False)
    # E.g., "Sunday-Thursday, 10:00-14:00"
    hours = Column(String, nullable=False)
    # E.g., Email or phone number
    contact_info = Column(String, nullable=True)

class ExamSchedule(Base):
    __tablename__ = "exam_schedules"

    id = Column(Integer, primary_key=True, index=True)
    # E.g., "Animation Final Project" or "System Analysis"
    course_name = Column(String, index=True, nullable=False)
    # Precise date and time of the exam/submission
    exam_date = Column(DateTime, nullable=False)
    # E.g., "Room 402"
    location = Column(String, nullable=False)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    # E.g., "Room 402", "Sewing Workshop"
    room_name = Column(String, index=True, nullable=False)
    building = Column(String, nullable=False)
    # E.g., "Has 3D printers, large cutting tables, and projectors"
    description = Column(Text, nullable=True)

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    # E.g., "How do I appeal a grade?"
    question = Column(String, nullable=False)
    # The official answer
    answer = Column(Text, nullable=False)
    # E.g., "Registration", "Exams", "General"
    tags = Column(String, nullable=True)