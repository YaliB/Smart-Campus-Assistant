import pytest
from unittest.mock import AsyncMock, patch
from services.ai_service import get_ai_response

@pytest.mark.asyncio
async def test_get_ai_response_success():
    """
    Test a successful AI response parsing.
    We mock the OpenAI client to return a valid JSON string.
    """
    # Mock data that mimics OpenAI's response format
    mock_content = '{"answer": "The exam is on June 20th", "category": "Schedule"}'
    
    # We patch the OpenAI client inside the ai_service module
    with patch("services.ai_service.client.chat.completions.create", new_callable=AsyncMock) as mock_create:
        # Define what the mock should return
        mock_create.return_value.choices[0].message.content = mock_content
        
        # Execute the function
        result = await get_ai_response("When is the exam?", "Local context about exams")
        
        # Assertions
        assert result["answer"] == "The exam is on June 20th"
        assert result["category"] == "Schedule"
        mock_create.assert_called_once()

@pytest.mark.asyncio
async def test_get_ai_response_fallback():
    """
    Test the fallback mechanism when the AI service fails.
    """
    # We force the mock to raise an exception
    with patch("services.ai_service.client.chat.completions.create", side_effect=Exception("API connection failed")):
        result = await get_ai_response("When is the exam?", "Context")
        
        # Verify it returns the friendly error message we defined in the service
        assert "currently unavailable" in result["answer"]
        assert result["category"] == "Technical"