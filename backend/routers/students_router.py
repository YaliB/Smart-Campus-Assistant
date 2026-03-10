from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

# Import Pydantic schemas for data validation
from ..api_models.api_ask_schemas import AskRequest, AskResponse
# Database imports
from ..database.db import get_db
from ..database.db_models import User
# Services imports
from ..services.auth_service import get_current_user
from ..services.db_service import get_relevant_context
from ..services.ai_service import get_ai_response
from ..services.api_rate_limit import limiter

# Initialize the router
router = APIRouter()

@router.post("/ask", response_model=AskResponse)
@limiter.limit("5/minute") # Rate limit: 5 questions per minute per user (identified by JWT token or IP address)
async def ask_question(
    request: Request, # needed to access the client's IP for rate limiting
    payload: AskRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # This makes the endpoint protected. Only registered users with a valid JWT token can access it. 
    ):
    """
    Main endpoint for the Smart Campus Assistant.
    Receives a student's question, retrieves local context, and generates an AI response.
    """
    try:
        # Step 1: Extract the question from the validated payload
        user_question = payload.question
        
        # Step 2: Query the database for relevant information (Context)
        local_context = get_relevant_context(db=db, user_question=user_question)
        
        # Step 3: Send the question and context to the AI service asynchronously
        ai_result = await get_ai_response(user_question=user_question, context=local_context)
        
        # Step 4: Construct and return the final response
        # used .get() to safely extract the keys, providing fallbacks just in case
        return AskResponse(
            answer=ai_result.get("answer", "I couldn't generate a proper response at this time."),
            category=ai_result.get("category", "General")
        )

    except Exception as e:
        # Log the error (in the future, will use a logging library) TODO: Implement proper logging instead of print statements
        print(f"Error processing the /ask request: {e}")
        
        # Return a 500 Internal Server Error to the client
        raise HTTPException(
            status_code=500, 
            detail="An internal server error occurred while processing your question."
        )