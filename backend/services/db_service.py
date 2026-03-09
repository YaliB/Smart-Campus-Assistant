from sqlalchemy.orm import Session
from sqlalchemy import or_
from database.db_models import FAQ, Room, ExamSchedule, ReceptionHour

def get_relevant_context(db: Session, user_question: str) -> str:
    """
    Searches the database for information relevant to the user's question.
    Extracts keywords and queries all campus tables to build a unified context string.
    """
    # 1. Basic keyword extraction (ignoring common Hebrew/English stop words)
    stop_words = ["what", "where", "when", "how", "is", "the", "a", "to", "in", "of", "and",
                  "מה", "איפה", "מתי", "איך", "האם", "זה", "של", "את", "ב", "ל", "ה", "יש"]
    
    # Keep words that are not in the stop_words list and are longer than 2 characters
    keywords = [word for word in user_question.split() if word not in stop_words and len(word) > 2]
    
    if not keywords:
        # Fallback: if no meaningful keywords found, use the original string
        keywords = [user_question]

    context_parts = []

    # 2. Search in FAQs
    faq_results = db.query(FAQ).filter(
        or_(*[FAQ.question.ilike(f"%{kw}%") for kw in keywords]) |
        or_(*[FAQ.tags.ilike(f"%{kw}%") for kw in keywords])
    ).limit(3).all()
    
    if faq_results:
        context_parts.append("General Information & FAQs:")
        for faq in faq_results:
            context_parts.append(f"- Q: {faq.question} | A: {faq.answer}")

    # 3. Search in Rooms
    room_results = db.query(Room).filter(
        or_(*[Room.room_name.ilike(f"%{kw}%") for kw in keywords]) |
        or_(*[Room.description.ilike(f"%{kw}%") for kw in keywords])
    ).limit(3).all()
    
    if room_results:
        context_parts.append("Campus Locations:")
        for room in room_results:
            context_parts.append(f"- {room.room_name} ({room.building}): {room.description}")

    # 4. Search in Exam Schedules
    exam_results = db.query(ExamSchedule).filter(
        or_(*[ExamSchedule.course_name.ilike(f"%{kw}%") for kw in keywords])
    ).limit(3).all()
    
    if exam_results:
        context_parts.append("Exam & Submission Schedules:")
        for exam in exam_results:
            # Format the datetime object to a readable string
            exam_time_str = exam.exam_date.strftime('%Y-%m-%d %H:%M')
            context_parts.append(f"- {exam.course_name}: {exam_time_str} at {exam.location}")

    # 5. Search in Reception Hours
    reception_results = db.query(ReceptionHour).filter(
        or_(*[ReceptionHour.department.ilike(f"%{kw}%") for kw in keywords])
    ).limit(3).all()
    
    if reception_results:
        context_parts.append("Reception Hours:")
        for rec in reception_results:
            context_parts.append(f"- {rec.department}: {rec.hours} (Contact: {rec.contact_info})")

    # 6. Combine all found context into a single string
    if not context_parts:
        return "No specific local context found in the database."
        
    return "\n".join(context_parts)