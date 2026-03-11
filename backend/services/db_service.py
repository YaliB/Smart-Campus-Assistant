from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from deep_translator import GoogleTranslator
from ..database.db_models import FAQ, Room, ExamSchedule, ReceptionHour

def get_relevant_context(db: Session, user_question: str) -> str:
    """Retrieves and assembles contextual information from the database to answer a user query.
    
    This function implements a **Two-Step Fallback Strategy** to ensure robust and comprehensive
    search results across multiple database entities. The workflow is as follows:
    
    1. **Language Translation**: The user's question is automatically translated from any language
       (e.g., Hebrew) to English using the Google Translate API. This enables multilingual query
       support by standardizing all searches against English-indexed database fields.
    
    2. **Keyword Extraction**: The translated question is cleaned (removing punctuation and
       stop words) to extract semantically meaningful keywords. These keywords form the basis
       for database searches.
    
    3. **Two-Step Fallback Search** (applied to each entity type):
       - **Step 1 (Strict AND)**: Queries the database requiring ALL keywords to match (AND logic).
         This ensures high precision by returning only highly relevant results.
       - **Step 2 (Fallback OR)**: If Step 1 returns no results, the search automatically relaxes
         to OR logic, requiring ANY keyword to match. This increases recall and ensures users
         receive helpful information even if exact multi-keyword matches don't exist.
    
    4. **Multi-Entity Search**: The function queries four database entities in sequence:
       - FAQ (Frequently Asked Questions)
       - Room (Campus locations and facilities)
       - ExamSchedule (Exam dates, times, and locations)
       - ReceptionHour (Department reception hours and contact information)
    
    5. **Context Assembly**: Results from all entities are formatted and combined into a
       single context string, labeled by entity type for clarity.
    
    Args:
        db (Session): A SQLAlchemy database session object used to execute queries against
            the database. This session must be active and connected to the database.
        user_question (str): The student's question in any language (e.g., Hebrew, English).
            The function automatically detects and translates the language to English for
            standardized database searches.
    
    Returns:
        str: A formatted context string containing search results from the database, organized
            by entity type (FAQs, Locations, Exam Schedules, Reception Hours). Each line
            contains formatted information (e.g., "- Room Name (Building): Description"). If no
            results are found in any entity, returns the fallback message:
            "No specific local context found in the database."
    
    Raises:
        No exceptions are explicitly raised. If translation fails (e.g., no internet connection),
        the function gracefully falls back to using the original user question for database
        searches. Database query failures are not caught; they propagate to the caller.
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
    # Two-Step Fallback Strategy: First try strict AND, then fallback to OR.

    # --- General Information & FAQs ---
    # Step 1: Strict AND search for maximum accuracy
    faq_and_conditions = [or_(FAQ.question.ilike(f"%{kw}%"), FAQ.tags.ilike(f"%{kw}%")) for kw in keywords]
    faq_results = db.query(FAQ).filter(and_(*faq_and_conditions)).limit(5).all()
    
    # Step 2: Fallback to OR with a larger limit if nothing is found
    if not faq_results:
        faq_or_conditions = [or_(FAQ.question.ilike(f"%{kw}%"), FAQ.tags.ilike(f"%{kw}%")) for kw in keywords]
        faq_results = db.query(FAQ).filter(or_(*faq_or_conditions)).limit(15).all()

    if faq_results:
        context_parts.append("General Information & FAQs:")
        for faq in faq_results:
            context_parts.append(f"- Q: {faq.question} | A: {faq.answer}")

    # --- Campus Locations ---
    room_and_conditions = [or_(Room.room_name.ilike(f"%{kw}%"), Room.description.ilike(f"%{kw}%")) for kw in keywords]
    room_results = db.query(Room).filter(and_(*room_and_conditions)).limit(5).all()
    
    if not room_results:
        room_or_conditions = [or_(Room.room_name.ilike(f"%{kw}%"), Room.description.ilike(f"%{kw}%")) for kw in keywords]
        room_results = db.query(Room).filter(or_(*room_or_conditions)).limit(15).all()

    if room_results:
        context_parts.append("Campus Locations:")
        for room in room_results:
            context_parts.append(f"- {room.room_name} ({room.building}): {room.description}")

    # --- Exam & Submission Schedules ---
    exam_and_conditions = [ExamSchedule.course_name.ilike(f"%{kw}%") for kw in keywords]
    exam_results = db.query(ExamSchedule).filter(and_(*exam_and_conditions)).limit(5).all()
    
    if not exam_results:
        exam_or_conditions = [ExamSchedule.course_name.ilike(f"%{kw}%") for kw in keywords]
        exam_results = db.query(ExamSchedule).filter(or_(*exam_or_conditions)).limit(15).all()
    
    if exam_results:
        context_parts.append("Exam & Submission Schedules:")
        for exam in exam_results:
            exam_time_str = exam.exam_date.strftime('%Y-%m-%d %H:%M')
            context_parts.append(f"- {exam.course_name}: {exam_time_str} at {exam.location}")

    # --- Reception Hours ---
    rec_and_conditions = [ReceptionHour.department.ilike(f"%{kw}%") for kw in keywords]
    reception_results = db.query(ReceptionHour).filter(and_(*rec_and_conditions)).limit(5).all()
    
    if not reception_results:
        rec_or_conditions = [ReceptionHour.department.ilike(f"%{kw}%") for kw in keywords]
        reception_results = db.query(ReceptionHour).filter(or_(*rec_or_conditions)).limit(15).all()
    
    if reception_results:
        context_parts.append("Reception Hours:")
        for rec in reception_results:
            context_parts.append(f"- {rec.department}: {rec.hours} (Contact: {rec.contact_info})")
            
    # 5. Return the combined context
    if not context_parts:
        return "No specific local context found in the database."

    return "\n".join(context_parts)