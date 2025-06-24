import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from .agents.career_graph import create_career_planning_graph
from .models.state import UserQuery, CareerPlanResponse

# Set up logging for uvicorn - this is crucial for seeing logs in terminal
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="CareerPath.AI",
    description="AI-powered career planning with multi-agent system",
    version="1.0.0"
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the multi-agent system
career_graph = None
try:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logger.error("❌ OPENAI_API_KEY not found in environment variables")
        logger.info("🔧 Please set your OPENAI_API_KEY environment variable")
    else:
        career_graph = create_career_planning_graph(openai_api_key)
        logger.info("✅ Multi-agent career planning system initialized successfully!")
except Exception as e:
    logger.error(f"❌ Failed to initialize career planning system: {str(e)}")

@app.get("/")
async def root():
    """Root health check endpoint"""
    logger.info("🏠 Root endpoint accessed")
    return {
        "message": "CareerPath.AI Backend is running!",
        "status": "healthy",
        "agents_available": career_graph is not None
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    logger.info("🔍 Health check requested")
    return {
        "status": "healthy",
        "agents": {
            "supervisor": True,
            "skills_agent": True,
            "industry_agent": True,
            "learning_agent": True,
            "resources_agent": True
        },
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

# Chat message model for the simple chat endpoint
class ChatMessage(BaseModel):
    message: str
    conversation_history: Optional[list] = []
    current_learning_path: Optional[dict] = None
    is_follow_up: Optional[bool] = False

@app.post("/api/chat")
async def chat(chat_message: ChatMessage):
    """Enhanced chat endpoint with conversation context support"""
    logger.info(f"💬 Chat request: {chat_message.message[:100]}...")
    logger.info(f"🧠 Context: follow_up={chat_message.is_follow_up}, "
                f"history_len={len(chat_message.conversation_history)}, "
                f"has_existing_path={bool(chat_message.current_learning_path)}")
    
    if not career_graph:
        logger.warning("⚠️ Career planning system not available")
        return {
            "response": "Sorry, the career planning system is not available. Please check the OpenAI API key configuration.",
            "mermaid_chart": None,
            "data": None
        }
    
    try:
        logger.info("🤖 Processing request with multi-agent system...")
        
        # Pass conversation context to the career planning system
        result = career_graph.plan_career(
            user_message=chat_message.message,
            conversation_history=chat_message.conversation_history,
            existing_learning_path=chat_message.current_learning_path,
            is_follow_up=chat_message.is_follow_up
        )
        
        logger.info("✅ Career plan generated successfully")
        logger.debug(f"📊 Response contains learning path: {bool(result.get('learning_path'))}")
        logger.debug(f"📝 Response message length: {len(result.get('message', ''))}")
        
        # Detailed logging of the response being sent to frontend
        response_data = {
            "response": result["message"],
            "mermaid_chart": result.get("mermaid_chart"),
            "data": result
        }
        
        print("=" * 80)
        print("🚀 CONTEXTUAL RESPONSE BEING SENT TO FRONTEND:")
        print("=" * 80)
        print(f"📄 Response Text (first 200 chars): {response_data['response'][:200]}...")
        print(f"🧠 Context Used: follow_up={chat_message.is_follow_up}")
        print(f"📊 Learning Path Present: {bool(response_data['data'].get('learning_path'))}")
        if response_data['data'].get('learning_path'):
            path = response_data['data']['learning_path']
            phases = path.get('learning_phases', [])
            print(f"🎯 Learning Phases Count: {len(phases)}")
            if phases:
                print("📚 Phase Names:", [p.get('phase', 'Unnamed') for p in phases[:3]])
        print("💾 Full Data Keys:", list(response_data['data'].keys()) if response_data['data'] else "None")
        print("=" * 80)
        
        return response_data
        
    except Exception as e:
        logger.error(f"❌ Error in chat endpoint: {str(e)}")
        print(f"🔴 ERROR IN CHAT ENDPOINT: {str(e)}")
        return {
            "response": f"I encountered an error while processing your request: {str(e)}",
            "mermaid_chart": None,
            "data": None
        }

@app.post("/api/career-plan", response_model=dict)
async def create_career_plan(query: UserQuery):
    """Generate a comprehensive career plan using multi-agent system"""
    logger.info(f"🎯 Career plan request: {query.message[:100]}...")
    logger.debug(f"📍 Current role: {query.current_role}, Target role: {query.target_role}")
    
    if not career_graph:
        logger.error("❌ Career planning system not initialized")
        raise HTTPException(status_code=500, detail="Career planning system not available")
    
    try:
        logger.info("🚀 Starting multi-agent career planning process...")
        result = career_graph.plan_career(
            user_message=query.message,
            current_role=query.current_role,
            target_role=query.target_role
        )
        
        logger.info("✅ Career plan generated successfully")
        logger.debug(f"📊 Mermaid chart length: {len(result.get('mermaid_chart', ''))}")
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating career plan: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate career plan: {str(e)}"
        ) 