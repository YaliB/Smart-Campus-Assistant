from datetime import datetime
from database.db import SessionLocal
from database.db_models import ReceptionHour, ExamSchedule, FAQ, Room

def seed_data():
    db = SessionLocal()
    
    try:
        print("Starting to seed database with rich campus data...")

        # --- 1. Reception Hours ---
        receptions = [
            ReceptionHour(department="Academic Secretariat", hours="Sunday to Thursday, 09:00 - 13:00", contact_info="secretariat@shenkar.ac.il"),
            ReceptionHour(department="IT Support", hours="Sunday to Thursday, 08:00 - 18:00", contact_info="helpdesk@shenkar.ac.il"),
            ReceptionHour(department="Design Faculty Office", hours="Monday and Wednesday, 10:00 - 14:00", contact_info="design@shenkar.ac.il"),
            ReceptionHour(department="Student Union", hours="Sunday to Thursday, 10:00 - 15:00", contact_info="aguda@shenkar.ac.il")
        ]

        # --- 2. Rooms ---
        rooms = [
            Room(room_name="Room 402", building="Main Building", description="Computer lab equipped with advanced design and 3D software."),
            Room(room_name="Room 215", building="Mitchell Building", description="Animation studio with light tables and rendering stations."),
            Room(room_name="Library", building="Pernick Building", description="Central library with quiet study zones and printing services."),
            Room(room_name="Auditorium 1", building="Main Building", description="Large lecture hall for guest lectures, presentations, and screenings."),
            Room(room_name="Room 310", building="Mitchell Building", description="Video editing and interactive media lab.")
        ]

        # --- 3. Exams & Schedule ---
        exams = [
            ExamSchedule(course_name="System Analysis", exam_date=datetime(2026, 6, 20, 10, 0), location="Room 402"),
            ExamSchedule(course_name="The Designer as Image Creator", exam_date=datetime(2026, 7, 5, 9, 0), location="Room 310"),
            ExamSchedule(course_name="Interactive Project Presentation", exam_date=datetime(2026, 7, 12, 11, 30), location="Auditorium 1"),
            ExamSchedule(course_name="Final Animation Storyboard Review", exam_date=datetime(2026, 7, 15, 10, 0), location="Room 215")
        ]

        # --- 4. FAQs ---
        faqs = [
            FAQ(question="What can you do?", answer="I can help you find useful information about campus. Try asking me where a certain place is, when a certain test is held, opening hours or just a general question I'm here for you! :)", tags="help, Capabilities, General"),
            FAQ(question="How do I register for courses?", answer="Registration is done through the student portal during the designated windows. Make sure you have paid the tuition advance.", tags="Registration, Portal, Tuition"),
            FAQ(question="Can I borrow video equipment?", answer="Yes, students taking video or animation courses can borrow cameras and tripods from the media center in the Mitchell building with their student ID.", tags="Equipment, Video, Media, Borrow"),
            FAQ(question="How do I connect to the campus Wi-Fi?", answer="Select 'Campus-Net' from your device and log in using your standard student email and password.", tags="IT, Wifi, Internet, Network"),
            FAQ(question="Where can I get help with my Interactive project?", answer="The interactive labs are open for free work every evening from 18:00 to 21:00. Teaching assistants are available on Tuesdays.", tags="Interactive, Lab, Help, TA"),
            FAQ(question="Is there parking on campus?", answer="Student parking is available in the underground lot of the Pernick building. A valid student parking sticker is required to enter.", tags="Parking, Transport, Car")
        ]

        # upload all data to the database
        db.add_all(receptions)
        db.add_all(rooms)
        db.add_all(exams)
        db.add_all(faqs)
        
        # commit all changes at once for efficiency and to ensure data integrity
        db.commit()
        print("✅ Database seeded successfully with a rich dataset!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()