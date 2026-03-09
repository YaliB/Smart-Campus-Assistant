import os
from datetime import datetime
from sqlalchemy.orm import Session
from ..database.db import SessionLocal
from ..database.db_models import User, ReceptionHour, ExamSchedule, FAQ, Room
from ..services.auth_service import get_password_hash, verify_password


def init_root_admin(db: Session):
    """
    Ensures the root admin user exists based on .env configuration.
    Called once during application startup.
    """
    root_email = os.getenv("ROOT_ADMIN_EMAIL", "root@campus.ac.il")
    root_pass = os.getenv("ROOT_ADMIN_PASSWORD", "admin123")
    
    user = db.query(User).filter(User.email == root_email).first()
    
    if not user:
        hashed_pw = get_password_hash(root_pass)
        new_root = User(email=root_email, hashed_password=hashed_pw, is_admin=True, student_id="00000000")
        db.add(new_root)
        db.commit()
        print(f"[*] Bootstrapped ROOT Admin: {root_email}")
    else:
        if not verify_password(root_pass, user.hashed_password):
            user.hashed_password = get_password_hash(root_pass)
            db.commit()
            print("[*] ROOT Admin password updated from .env")
        
        if not user.is_admin:
            user.is_admin = True
            db.commit()
            print("[*] Restored admin privileges to ROOT Admin")


# This function is intended to be called once to populate the database with initial data for testing and development purposes. 
def seed_data():
    db = SessionLocal()
    
    # Adding a sample reception hour [cite: 9]
    secretariat = ReceptionHour(
        department="Academic Secretariat",
        hours="Sunday to Thursday, 09:00 - 13:00",
        contact_info="info@shenkar.ac.il"
    )
    
    # Adding a sample exam schedule [cite: 7]
    exam = ExamSchedule(
        course_name="System Analysis",
        exam_date=datetime(2026, 6, 20, 10, 0),
        location="Room 402"
    )
    
    # Adding a sample FAQ [cite: 13]
    faq = FAQ(
        question="How do I register for courses?",
        answer="Registration is done through the student portal during the designated windows.",
        tags="Registration"
    )

    # Adding a sample room [cite: 8]
    room = Room(
        room_name="Room 402",
        building="Main Building",
        description="Computer lab equipped with design software."
    )

    db.add_all([secretariat, exam, faq, room])
    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()