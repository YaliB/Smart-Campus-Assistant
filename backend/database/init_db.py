from datetime import datetime
from database.database import SessionLocal
from database.db_models import ReceptionHour, ExamSchedule, FAQ, Room

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