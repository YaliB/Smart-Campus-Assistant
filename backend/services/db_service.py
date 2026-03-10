from sqlalchemy.orm import Session
from sqlalchemy import or_
from deep_translator import GoogleTranslator
from ..database.db_models import FAQ, Room, ExamSchedule, ReceptionHour

def get_relevant_context(db: Session, user_question: str) -> str:
    """
    Translates the user's question to English dynamically, extracts keywords,
    and searches the database to support multilingual queries.
    """
    # 1. Translate the original question to English using a free translator
    try:
        # source='auto' automatically detects Hebrew (or any language)
        translated_question = GoogleTranslator(source='auto', target='en').translate(user_question)
    except Exception as e:
        print(f"Translation failed: {e}")
        # Fallback to the original question if translation fails (e.g., no internet)
        translated_question = user_question 

    # 2. Preprocess the TRANSLATED question: Remove punctuation and special characters
    # This prevents Google Translate from appending '?' to keywords
    clean_translated = translated_question
    for char in "?.,!;:()[]{}-\"\'":
        clean_translated = clean_translated.replace(char, "")

    # 3. Extract keywords from the cleaned translated question, ignoring common stop words
    stop_words = {"what", "where", "when", "how", "is", "the", "a", "to", "in", "of", "and", "are", "do", "does", "for"}
    
    # Keep only meaningful keywords (length > 2 and not in stop words)
    keywords = [word for word in clean_translated.split() if word.lower() not in stop_words and len(word) > 2]
    
    if not keywords:
        # Fallback if no meaningful keywords remain
        keywords = clean_translated.split() # Use all words if no keywords extracted

    context_parts = []

    # 4. Search the Database using the ENGLISH keywords
    faq_results = db.query(FAQ).filter(
        or_(*[FAQ.question.ilike(f"%{kw}%") for kw in keywords]) |
        or_(*[FAQ.tags.ilike(f"%{kw}%") for kw in keywords])
    ).limit(3).all()
    
    if faq_results:
        context_parts.append("General Information & FAQs:")
        for faq in faq_results:
            context_parts.append(f"- Q: {faq.question} | A: {faq.answer}")

    room_results = db.query(Room).filter(
        or_(*[Room.room_name.ilike(f"%{kw}%") for kw in keywords]) |
        or_(*[Room.description.ilike(f"%{kw}%") for kw in keywords])
    ).limit(3).all()
    
    if room_results:
        context_parts.append("Campus Locations:")
        for room in room_results:
            context_parts.append(f"- {room.room_name} ({room.building}): {room.description}")

    exam_results = db.query(ExamSchedule).filter(
        or_(*[ExamSchedule.course_name.ilike(f"%{kw}%") for kw in keywords])
    ).limit(3).all()
    
    if exam_results:
        context_parts.append("Exam & Submission Schedules:")
        for exam in exam_results:
            exam_time_str = exam.exam_date.strftime('%Y-%m-%d %H:%M')
            context_parts.append(f"- {exam.course_name}: {exam_time_str} at {exam.location}")

    reception_results = db.query(ReceptionHour).filter(
        or_(*[ReceptionHour.department.ilike(f"%{kw}%") for kw in keywords])
    ).limit(3).all()
    
    if reception_results:
        context_parts.append("Reception Hours:")
        for rec in reception_results:
            context_parts.append(f"- {rec.department}: {rec.hours} (Contact: {rec.contact_info})")

    print(f"Context retrieved for question: '{user_question}' (Translated: '{translated_question}')")
    print(f"Extracted Keywords: {keywords}")
    print (f"Context Parts Found: {len(context_parts)}")
            
    # 5. Return the combined context
    if not context_parts:
        return "No specific local context found in the database."

    return "\n".join(context_parts)