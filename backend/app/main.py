from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json # Added for JSON parsing
from pathlib import Path
from dotenv import load_dotenv

# Import OpenAI Agents SDK components
from agents import Agent, Runner
import asyncio # Runner.run is often async

# Load environment variables
project_root = Path(__file__).resolve().parent.parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path)

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",         # Allow localhost (common for dev)
    "http://localhost:5173",    # Default Vite dev server port
    "http://127.0.0.1:5173",  # Another way to refer to localhost
    # Add any other origins you might use, like your production frontend URL eventually
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# INITIAL_PROMPT for the Career Path AI Agent (remains largely the same)
INITIAL_PROMPT = """You are a friendly, empathetic career guidance expert at CareerPath.AI. 
Your style is concise, warm, and supportive.

You will be provided with the conversation history as a list of messages (user and assistant roles) followed by the current user message.
Use this history to maintain context and provide relevant guidance.

Follow these guidelines strictly:
1. Keep your responses brief and to the point - use 1-3 short paragraphs maximum.
2. Ask only one clear, focused question at a time.
3. Be emotionally intelligent - recognize signs of frustration, uncertainty, or demotivation and respond with empathy.
4. Provide actionable, practical steps for each career path you suggest.
5. Tailor your advice to the user's specific circumstances, skills, and interests.
6. When suggesting resources, be specific (books, courses, websites).
7. When you have enough information to suggest a career path or a set of learning steps, you MUST format this as a JSON object within your response, prefixed by "ROADMAP_DATA:" and followed by the JSON.
   The JSON should have a key "title" for the roadmap and a key "steps", which is a list of objects. Each step object should have "id" (string, e.g., "step1"), "title" (string), "description" (string), and optionally "resources" (list of objects with "type", "name", "url") and "sub_steps" (list of step objects).

Example of roadmap JSON structure:
ROADMAP_DATA:
{
  "title": "Frontend Developer Roadmap",
  "steps": [
    {
      "id": "1",
      "title": "Learn HTML",
      "description": "Understand the basic structure of web pages.",
      "resources": [
        {"type": "course", "name": "HTML Crash Course", "url": "http://example.com/html"}
      ]
    },
    {
      "id": "2",
      "title": "Learn CSS",
      "description": "Style your web pages.",
      "sub_steps": [
        {
          "id": "2.1",
          "title": "CSS Basics",
          "description": "Selectors, properties."
        },
        {
          "id": "2.2",
          "title": "Flexbox & Grid",
          "description": "For layout."
        }
      ]
    }
  ]
}

When the user expresses negative emotions or doubts:
- Acknowledge their feelings first.
- Offer reassurance and perspective.
- Share a practical next step they can take.

Maintain a conversational, friendly tone while being professional and direct."""

# Initialize the Career Path Agent
# The openai-agents SDK will use the OPENAI_API_KEY environment variable by default.
# You might specify a model using model_config if needed, e.g., model_config={"model": "gpt-4o"}
career_path_agent = Agent(
    name="CareerPathAgent",
    instructions=INITIAL_PROMPT
)

# In-memory session store for conversation history
user_sessions = {} 

class ChatMessage(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    reply: str
    roadmap_data: dict | None = None

async def get_agent_response(session_id: str, user_message: str):
    if not os.getenv("OPENAI_API_KEY"):
        return {"error": "OPENAI_API_KEY not found or not configured on the server."}

    # Retrieve or initialize conversation history from user_sessions
    # History for the agent should be a list of message dicts: {"role": "user/assistant", "content": "..."}
    # The system prompt is handled by the agent's instructions.
    history = user_sessions.get(session_id, [])
    
    # Construct messages for the agent run: history + current user message
    messages_for_agent_run = history + [{"role": "user", "content": user_message}]

    try:
        # Use the Runner to execute the agent
        # The agent is passed as the first positional argument.
        # The input_data (messages) is passed as the second positional argument.
        # The agent's 'instructions' will serve as the system message.
        agent_result = await Runner.run(career_path_agent, messages_for_agent_run)
        full_response_text = agent_result.final_output

        if not isinstance(full_response_text, str):
            # Fallback or error if the output is not a string as expected
            print(f"Unexpected agent output type: {type(full_response_text)}. Output: {full_response_text}")
            full_response_text = str(full_response_text) # Try to cast

        # Update history in user_sessions
        updated_history = history + [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": full_response_text} # Store the raw response
        ]
        user_sessions[session_id] = updated_history

        # Extract roadmap JSON (same logic as before)
        roadmap_json = None
        reply_text_for_user = full_response_text # Default to full text

        if "ROADMAP_DATA:" in full_response_text:
            try:
                parts = full_response_text.split("ROADMAP_DATA:", 1)
                reply_text_for_user = parts[0].strip() # Text before ROADMAP_DATA
                json_str_part = parts[1].strip()
                
                json_start = json_str_part.find('{')
                json_end = json_str_part.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    actual_json_str = json_str_part[json_start:json_end]
                    roadmap_json = json.loads(actual_json_str)
                else: # Malformed JSON signal or no JSON braces
                    print(f"Could not find valid JSON structure in: {json_str_part}")
                    # Keep reply_text_for_user as the part before ROADMAP_DATA, roadmap_json remains None
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e} - JSON part: {json_str_part}")
                # Error in parsing, reply_text_for_user is already set, roadmap_json remains None
            except Exception as e:
                print(f"Error during JSON extraction: {e}")
                # Fallback, roadmap_json remains None

        return {"reply": reply_text_for_user, "roadmap_data": roadmap_json}

    except Exception as e:
        print(f"An error occurred with the OpenAI Agent: {str(e)}")
        # Check for specific OpenAI API errors if needed, e.g., authentication, rate limits
        return {"error": f"An error occurred while processing your request: {str(e)}"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    if not os.getenv("OPENAI_API_KEY"):
        return ChatResponse(reply="Error: OPENAI_API_KEY not configured on the server.", roadmap_data=None)

    response_data = await get_agent_response(chat_message.session_id, chat_message.message)
    
    if "error" in response_data:
        return ChatResponse(reply=response_data["error"], roadmap_data=None)
        
    return ChatResponse(reply=response_data["reply"], roadmap_data=response_data.get("roadmap_data"))

@app.get("/")
async def root():
    return {"message": "CareerPath.AI Backend with OpenAI Agents is running!"}

# Example for running with uvicorn (optional, usually run from terminal)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000) 