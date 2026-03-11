import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the asynchronous OpenAI client
# It automatically picks up the OPENAI_API_KEY from the environment
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

async def get_ai_response(user_question: str, context: str) -> dict:
    """Generates an AI response to a user question using context from the database.
    
    This function orchestrates the core AI interaction flow by sending the user's question
    and retrieved local context to the GPT-4o-mini model. The model is explicitly instructed
    to answer ONLY based on the provided context to prevent hallucinations and ensure
    accurate, factually-grounded responses. The model categorizes the response and enforces
    strict bilingual language compliance (responding in the same language as the user's question).
    
    The function implements a robust exception-handling fallback mechanism: if the OpenAI API
    is unavailable, times out, or returns invalid JSON, a graceful fallback response is returned.
    This ensures the assistant remains operational even during service disruptions.
    
    Args:
        user_question (str): The student's question in any language (e.g., Hebrew or English).
            The AI will automatically detect the language and respond in the same language.
        context (str): The retrieved local database context containing relevant FAQs, exam
            schedules, room locations, and reception hours. This context is formatted as a
            plain text string with labeled sections (e.g., "General Information & FAQs:").
    
    Returns:
        dict: A dictionary with two keys:
            - 'answer' (str): The AI-generated response to the user's question, or a fallback
              message if the API fails. The answer is guaranteed to be in the same language
              as the user's question.
            - 'category' (str): One of ['Schedule', 'Location', 'General', 'Technical'].
              Indicates the type of query for frontend routing and analytics.
    
    Raises:
        No exceptions are raised; all errors are caught and handled internally. If an exception
        occurs during the API call (network timeout, invalid JSON, API error), the function
        returns a fallback response with category 'Technical'.
    """
    
    # Define the system prompt with strict rules for the AI
    system_prompt = f"""
    You are the 'Smart Campus Assistant', a helpful and polite AI for university students.
    
    CRITICAL RULES:
    1. You must answer the student's question based ONLY on the provided 'Local Context'. 
       CRUCIAL BILINGUAL RULE: The Local Context is provided in English. If the user's question is in Hebrew (or any other language), you MUST mentally translate the concepts to find the matching information in the English context before giving up!
       
    2. If the answer cannot be found in the context, DO NOT guess or invent information. Instead, use the fallback message: 
       "I'm sorry, I don't have that information right now. Please contact the academic secretariat for further assistance."
       
    3. Categorize the user's question into EXACTLY one of the following categories:
       - "Schedule" (for exams, deadlines, or hours)
       - "Location" (for finding rooms or facilities)
       - "General" (for procedures, FAQs, or anything else)
       - "Technical" (for IT or system issues)
       
    4. LANGUAGE STRICT ENFORCEMENT: Your final response in the 'answer' field MUST BE IN THE EXACT SAME LANGUAGE the user used. If the user asks in Hebrew, you MUST translate your final answer back to Hebrew.
    
    5. DETAIL ENFORCEMENT: You must include ALL specific details provided in the context. Never omit Building names, exact dates, hours, or locations.
       
    OUTPUT FORMAT:
    You must respond in valid JSON format containing exactly two keys: 'answer' and 'category'.
    
    Local Context:
    {context}
    """

    print(f"Context being sent to the AI: {context}") # Debugging line to check the context being sent to the AI TODO : Remove

    try:
        # Make the asynchronous call to the OpenAI API
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={ "type": "json_object" }, # Forces the AI to return valid JSON
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User question (MUST answer in the exact language of this question!): {user_question}"}
            ],
            temperature=0.3, # Low temperature makes the AI more deterministic and focused
            max_tokens=250
        )
        
        # Extract the raw JSON string from the AI's response
        raw_content = response.choices[0].message.content
        
        # Parse the JSON string into a Python dictionary
        result_dict = json.loads(raw_content)
        print(f"AI response parsed successfully: {result_dict}") # Debugging line to check the parsed result TODO : Remove
        return result_dict

    except Exception as e:
        # Fallback mechanism in case the API fails, times out, or returns invalid JSON
        print(f"Error communicating with OpenAI: {e}")
        return {
            "answer": "The AI service is currently unavailable or busy. Please try again in a few minutes.",
            "category": "Technical"
        }