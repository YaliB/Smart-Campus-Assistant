from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import our database connection dependency
from database.database import get_db

# Import our Pydantic schemas for data validation
from backend.api_models.api_ask_schemas import AskRequest, AskResponse

# Import our business logic services
from services.db_service import get_relevant_context
from services.ai_service import get_ai_response

# Initialize the router
router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest, db: Session = Depends(get_db)):
    """
    Main endpoint for the Smart Campus Assistant.
    Receives a student's question, retrieves local context, and generates an AI response.
    """
    try:
        # Step 1: Extract the question from the validated request
        user_question = request.question
        
        # Step 2: Query the local database for relevant information (Context)
        # We pass the database session 'db' injected by FastAPI
        local_context = get_relevant_context(db=db, user_question=user_question)
        
        # Step 3: Send the question and context to the AI service asynchronously
        ai_result = await get_ai_response(user_question=user_question, context=local_context)
        
        # Step 4: Construct and return the final response
        # We use .get() to safely extract the keys, providing fallbacks just in case
        return AskResponse(
            answer=ai_result.get("answer", "I couldn't generate a proper response at this time."),
            category=ai_result.get("category", "General")
        )

    except Exception as e:
        # Log the error (in a real app, use a logging library) TODO: Implement proper logging instead of print statements
        print(f"Error processing the /ask request: {e}")
        
        # Return a 500 Internal Server Error to the client
        raise HTTPException(
            status_code=500, 
            detail="An internal server error occurred while processing your question."
        )