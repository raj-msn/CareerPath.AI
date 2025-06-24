from typing import Dict, List, Optional, Literal, Annotated, Any
from pydantic import BaseModel
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

class CareerPlanningState(TypedDict):
    """State for the career planning multi-agent system"""
    
    # Core conversation
    messages: List[BaseMessage]
    current_role: Optional[str]
    target_role: Optional[str]
    
    # Context for follow-up conversations
    conversation_history: Optional[List[Dict[str, str]]]
    existing_learning_path: Optional[Dict[str, Any]]
    is_follow_up: Optional[bool]
    
    # Agent outputs
    skills_assessment: Optional[Dict[str, Any]]
    industry_insights: Optional[Dict[str, Any]]
    learning_path: Optional[Dict[str, Any]]
    resources: Optional[Dict[str, Any]]
    mermaid_chart: Optional[str]
    next_agent: Optional[Literal["skills_agent", "industry_agent", "learning_agent", "resources_agent", "__end__"]] = None

class UserQuery(BaseModel):
    message: str
    current_role: Optional[str] = None
    target_role: Optional[str] = None

class CareerPlanResponse(BaseModel):
    message: str
    mermaid_chart: Optional[str] = None
    skills_gap: Optional[List[str]] = None
    recommended_resources: Optional[List[Dict]] = None 