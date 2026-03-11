import pytest
import json
from unittest.mock import AsyncMock, patch
from services.ai_service import get_ai_response

@pytest.mark.asyncio
async def test_get_ai_response_success():
    """Tests successful AI response generation and JSON parsing with valid context.
    
    This test verifies the happy-path scenario where the OpenAI API returns a well-formed JSON
    response object. The test mocks the OpenAI client to return a predefined JSON response
    containing both 'answer' and 'category' fields. It validates that the function correctly
    parses the JSON and returns a dictionary matching the mock content.
    
    Mock Setup:
        - Mocks `services.ai_service.client.chat.completions.create` to return a response
          with 'answer': "The exam is on June 20th" and 'category': "Schedule".
    
    Assertions:
        - Verifies the returned answer matches the expected value.
        - Verifies the returned category is correctly set to "Schedule".
        - Confirms that the OpenAI API mock was called exactly once.
    """
    mock_content = '{"answer": "The exam is on June 20th", "category": "Schedule"}'
    
    with patch("services.ai_service.client.chat.completions.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value.choices[0].message.content = mock_content
        result = await get_ai_response("When is the exam?", "Local context: The exam is on June 20th")
        
        assert result["answer"] == "The exam is on June 20th"
        assert result["category"] == "Schedule"
        mock_create.assert_called_once()

@pytest.mark.asyncio
async def test_get_ai_response_hebrew_translation_rule():
    """Tests enforcement of CRITICAL RULE 4: Language preservation in AI responses.
    
    This test validates that the AI service correctly enforces the bilingual language rule,
    which states that the AI must respond in the exact same language as the user's question.
    Even though the provided context is in English, the AI is expected to translate its answer
    back to the source language of the user's question (Hebrew in this case).
    
    This test is crucial for validating multilingual support in the Smart Campus Assistant,
    as students may ask questions in Hebrew while the database context is primarily in English.
    The test mocks the AI's behavior of translating the final answer back to Hebrew.
    
    Mock Setup:
        - Mocks `services.ai_service.client.chat.completions.create` to return a Hebrew response:
          'answer': "הבחינה מתקיימת ב-20 ביוני" (The exam is held on June 20th in Hebrew)
          'category': "Schedule".
        - The user question is provided in Hebrew: "מתי המבחן שלי?" (When is my exam?).
    
    Assertions:
        - Verifies that the returned answer contains Hebrew text (contains "הבחינה").
        - Verifies the category is correctly identified as "Schedule".
    """
    # Mocking the AI successfully translating the English context back to Hebrew
    mock_content = '{"answer": "הבחינה מתקיימת ב-20 ביוני", "category": "Schedule"}'
    
    with patch("services.ai_service.client.chat.completions.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value.choices[0].message.content = mock_content
        
        result = await get_ai_response("מתי המבחן שלי?", "Exam date: June 20th")
        
        assert "הבחינה" in result["answer"]
        assert result["category"] == "Schedule"

@pytest.mark.asyncio
async def test_get_ai_response_empty_context_fallback():
    """Tests enforcement of CRITICAL RULE 2: Graceful fallback for missing information.
    
    This test ensures that when the provided context does not contain information relevant to
    the user's question, the AI correctly returns a standardized fallback message instead of
    hallucinating or guessing. This is a critical feature to maintain accuracy and reliability
    of the Smart Campus Assistant.
    
    The test simulates a scenario where a user asks about information (e.g., pizza restaurants)
    that is entirely outside the scope of the campus database context. The AI is expected to
    recognize this and return a professional, helpful fallback message directing the student
    to contact the academic secretariat.
    
    Mock Setup:
        - Mocks `services.ai_service.client.chat.completions.create` to return the standardized
          fallback message when context is insufficient.
        - Provides context unrelated to the user's question to trigger the fallback behavior.
    
    Assertions:
        - Verifies that the returned answer contains the exact fallback text:
          "I'm sorry, I don't have that information right now. Please contact the academic secretariat for further assistance."
        - Verifies that the category is "General" for out-of-scope queries.
    """
    expected_fallback = "I'm sorry, I don't have that information right now. Please contact the academic secretariat for further assistance."
    mock_content = f'{{"answer": "{expected_fallback}", "category": "General"}}'
    
    with patch("services.ai_service.client.chat.completions.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value.choices[0].message.content = mock_content
        
        # User asks something completely unrelated to the provided context
        result = await get_ai_response("Where can I buy pizza?", "Context: Math exam is in Room 17")
        
        assert "academic secretariat" in result["answer"]
        assert result["category"] == "General"

@pytest.mark.asyncio
async def test_get_ai_response_invalid_json_handling():
    """Tests the exception-handling fallback when the AI returns malformed JSON.
    
    This test validates the robustness of the AI service against a common failure mode:
    the OpenAI API successfully responds, but the response contains invalid or malformed JSON
    that cannot be parsed by `json.loads()`. This can occur if the model ignores the
    "json_object" response format instruction and returns text or markdown instead.
    
    The test verifies that the function gracefully catches the JSON parsing exception and
    returns a fallback response, preventing the entire application from crashing due to
    a malformed API response.
    
    Mock Setup:
        - Mocks `services.ai_service.client.chat.completions.create` to return invalid JSON:
          'Here is your answer: { "answer": "Room 17" }' (not valid JSON).
        - This simulates the AI breaking its format constraint.
    
    Assertions:
        - Verifies that the function catches the JSONDecodeError and enters the exception handler.
        - Confirms that the returned category is "Technical" (indicating a service issue).
        - Confirms that the answer contains the failsafe message: "currently unavailable".
    """
    # The AI returns text that cannot be parsed by json.loads()
    invalid_json_content = 'Here is your answer: { "answer": "Room 17" }'
    
    with patch("services.ai_service.client.chat.completions.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value.choices[0].message.content = invalid_json_content
        
        result = await get_ai_response("Where is the math class?", "Math class is in Room 17")
        
        # Should fall into the except Exception block
        assert result["category"] == "Technical"
        assert "currently unavailable" in result["answer"]

@pytest.mark.asyncio
async def test_get_ai_response_network_timeout_or_failure():
    """Tests the exception-handling fallback when the OpenAI API is completely unavailable.
    
    This test validates the resilience of the AI service against network failures, API
    timeouts, rate limiting, and other catastrophic API failures. When the OpenAI API
    is unreachable or returns an error, the function must gracefully return a fallback
    response to prevent service degradation.
    
    The test simulates a realistic failure scenario (API connection timeout) to ensure
    that the exception-handling mechanism in `get_ai_response()` correctly catches all
    exceptions and returns a user-friendly fallback message.
    
    Mock Setup:
        - Mocks `services.ai_service.client.chat.completions.create` to raise an Exception:
          Exception("API connection timed out").
        - This simulates a network timeout or complete API unavailability.
    
    Assertions:
        - Verifies that the function catches the exception and enters the except block.
        - Confirms that the returned category is "Technical" (indicating a service issue).
        - Confirms that the answer contains the failsafe message: "currently unavailable",
          instructing the user to retry later.
    """
    with patch("services.ai_service.client.chat.completions.create", side_effect=Exception("API connection timed out")):
        result = await get_ai_response("When is the exam?", "Context")
        
        assert "currently unavailable" in result["answer"]
        assert result["category"] == "Technical"