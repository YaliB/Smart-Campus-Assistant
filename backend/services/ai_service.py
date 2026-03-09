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
    """
    Sends the user's question and the retrieved local context to the AI model.
    Instructs the model to answer based ONLY on the context, preventing hallucinations.
    Returns a dictionary with 'answer' and 'category'.
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
        return result_dict

    except Exception as e:
        # Fallback mechanism in case the API fails, times out, or returns invalid JSON
        print(f"Error communicating with OpenAI: {e}")
        return {
            "answer": "The AI service is currently unavailable or busy. Please try again in a few minutes.",
            "category": "Technical"
        }