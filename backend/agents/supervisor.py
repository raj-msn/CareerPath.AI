from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from typing import Literal
import json

from ..models.state import CareerPlanningState

class CareerSupervisorAgent:
    def __init__(self, model: ChatOpenAI):
        self.model = model
        self.system_prompt = """You are the Career Supervisor Agent, the orchestrator of a multi-agent career planning system.

Your role:
1. Analyze user requests to determine if this is a new career plan or a follow-up question
2. Decide which agents need to run based on the context and user's question
3. Route to appropriate agents: skills_agent, industry_agent, learning_agent, resources_agent
4. For follow-up questions, determine what needs to be updated or refined

CONTEXT AWARENESS:
- If is_follow_up=True and existing_learning_path exists, the user is asking to modify an existing plan
- If conversation_history exists, consider previous context
- Focus on what the user specifically wants to update or add

Agent Decision Logic:
- NEW PLAN: Run all agents (skills → industry → learning → resources)
- FOLLOW-UP asking about skills/gaps: Run skills_agent → learning_agent → resources_agent
- FOLLOW-UP asking about timeline/learning: Run learning_agent → resources_agent  
- FOLLOW-UP asking about resources/courses: Run resources_agent only
- FOLLOW-UP asking about industry/salary: Run industry_agent → learning_agent → resources_agent

Always respond with the agent name to route to first: skills_agent, industry_agent, learning_agent, or resources_agent.
Consider the context and be efficient - don't re-run agents unless their output needs updating."""

    def __call__(self, state: CareerPlanningState) -> Command[Literal["skills_agent", "industry_agent", "learning_agent", "resources_agent"]]:
        current_message = state["messages"][-1].content.lower()
        is_follow_up = state.get("is_follow_up", False)
        has_existing_path = bool(state.get("existing_learning_path"))
        conversation_history = state.get("conversation_history", [])
        
        # Analyze the user's request
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
CONTEXT:
- Is Follow-up: {is_follow_up}
- Has Existing Plan: {has_existing_path}
- Conversation History Length: {len(conversation_history)}
- Current Role: {state.get('current_role', 'Not specified')}
- Target Role: {state.get('target_role', 'Not specified')}

USER REQUEST: {current_message}

EXISTING PLAN SUMMARY: {self._summarize_existing_plan(state.get('existing_learning_path')) if has_existing_path else 'None'}

Based on this context, which agent should handle this request first?
Respond with ONLY the agent name: skills_agent, industry_agent, learning_agent, or resources_agent
""")
        ]
        
        response = self.model.invoke(messages)
        next_agent = response.content.strip().lower()
        
        # Validate and default
        valid_agents = ["skills_agent", "industry_agent", "learning_agent", "resources_agent"]
        if next_agent not in valid_agents:
            # Default logic based on keywords
            if any(word in current_message for word in ["skill", "gap", "learn", "ability"]):
                next_agent = "skills_agent"
            elif any(word in current_message for word in ["industry", "market", "salary", "demand"]):
                next_agent = "industry_agent"
            elif any(word in current_message for word in ["timeline", "phase", "roadmap", "path", "step"]):
                next_agent = "learning_agent"
            elif any(word in current_message for word in ["course", "resource", "book", "certification"]):
                next_agent = "resources_agent"
            else:
                next_agent = "skills_agent"  # Default start
        
        return Command(
            goto=next_agent,
            update={"next_agent": next_agent}
        )
    
    def _summarize_existing_plan(self, learning_path):
        """Create a brief summary of the existing learning path"""
        if not learning_path:
            return "None"
            
        phases = learning_path.get("learning_phases", [])
        if not phases:
            return "Basic plan without specific phases"
            
        phase_names = [p.get("phase", "Unnamed") for p in phases[:3]]
        timeline = learning_path.get("timeline", "No timeline specified")
        
        return f"Timeline: {timeline}, Phases: {', '.join(phase_names)}" 