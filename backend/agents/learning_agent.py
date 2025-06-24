from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from typing import Literal
import json

from ..models.state import CareerPlanningState

class LearningPathAgent:
    def __init__(self, model: ChatOpenAI):
        self.model = model
        self.system_prompt = """You are a Learning Path Agent, an expert learning strategist who creates and refines personalized career roadmaps.

Your role:
1. CREATE new step-by-step learning paths for initial requests
2. MODIFY and REFINE existing learning paths for follow-up questions
3. Generate React Flow compatible JSON structure for interactive visualization
4. Prioritize learning based on industry insights and user context

CONTEXT AWARENESS:
- If existing_learning_path is provided, this is a MODIFICATION request
- If is_follow_up=True, focus on refining rather than replacing
- Consider conversation_history to understand what the user wants to change

For NEW plans, respond with:
{
    "learning_phases": [
        {
            "phase": "Phase Name",
            "duration": "X months", 
            "skills": ["skill1", "skill2"],
            "description": "What to focus on"
        }
    ],
    "timeline": "6-12 months total",
    "milestones": ["milestone1", "milestone2"]
}

For MODIFICATIONS, respond with:
{
    "learning_phases": [...updated phases...],
    "timeline": "updated timeline",
    "milestones": [...updated milestones...],
    "changes_made": "Summary of what was modified"
}

Keep phases practical, actionable, and timeline-focused."""

    def _fix_mermaid_quotes(self, mermaid_chart):
        """Fix Mermaid chart to ensure all node text is properly quoted"""
        if not mermaid_chart:
            return mermaid_chart
            
        import re
        # Pattern to find nodes with unquoted text like A[Some Text] 
        # and replace with A["Some Text"]
        pattern = r'([A-Z])\[([^\[\]"]*)\]'
        
        def replace_quotes(match):
            node_id = match.group(1)
            text = match.group(2)
            # Only add quotes if text isn't already quoted
            if not (text.startswith('"') and text.endswith('"')):
                return f'{node_id}["{text}"]'
            return match.group(0)
        
        fixed_chart = re.sub(pattern, replace_quotes, mermaid_chart)
        return fixed_chart

    def __call__(self, state: CareerPlanningState) -> Command[Literal["resources_agent", "__end__"]]:
        skills_info = state.get("skills_assessment") or {}
        industry_info = state.get("industry_insights") or {}
        existing_path = state.get("existing_learning_path")
        is_follow_up = state.get("is_follow_up", False)
        conversation_history = state.get("conversation_history", [])
        user_message = state["messages"][-1].content if state["messages"] else ""
        
        # Create context-aware prompt
        context_info = f"""
Current Role: {state.get('current_role') or 'Software Engineer'}
Target Role: {state.get('target_role') or 'Senior Software Engineer'}
Is Follow-up Request: {is_follow_up}
Skills Assessment: {json.dumps(skills_info, indent=2)}
Industry Insights: {json.dumps(industry_info, indent=2)}
User's Current Request: {user_message}
"""

        if is_follow_up and existing_path:
            context_info += f"""
EXISTING LEARNING PATH TO MODIFY:
{json.dumps(existing_path, indent=2)}

INSTRUCTION: The user wants to modify their existing learning path. Focus on their specific request and update accordingly. Don't create a completely new plan - refine what exists.
"""
        else:
            context_info += "\nINSTRUCTION: Create a comprehensive new learning path from scratch."

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=context_info)
        ]
        
        response = self.model.invoke(messages)
        
        try:
            learning_data = json.loads(response.content)
            
            # Ensure required fields exist
            if "learning_phases" not in learning_data:
                raise ValueError("Missing learning_phases")
                
        except (json.JSONDecodeError, ValueError):
            # Fallback with a basic structure
            current_role = state.get('current_role') or 'Software Engineer'
            target_role = state.get('target_role') or 'Senior Software Engineer'
            
            if is_follow_up and existing_path:
                # Try to preserve existing structure and make minimal changes
                learning_data = existing_path.copy()
                learning_data["changes_made"] = "Applied user's requested modifications"
            else:
                # Create new fallback plan
                learning_data = {
                    "learning_phases": [
                        {
                            "phase": "Foundation Building",
                            "duration": "1-2 months",
                            "skills": ["Advanced Programming", "System Design"],
                            "description": "Build core technical skills for seniority."
                        },
                        {
                            "phase": "Leadership & Mentoring", 
                            "duration": "2-3 months",
                            "skills": ["Team Leadership", "Project Management", "Mentoring"],
                            "description": "Develop soft skills required for a senior role."
                        },
                        {
                            "phase": "Architecture & Specialization",
                            "duration": "2-3 months", 
                            "skills": ["Software Architecture", "Advanced System Design"],
                            "description": "Focus on high-level design and specialization."
                        }
                    ],
                    "timeline": "6-8 months total",
                    "milestones": ["Complete system design course", "Lead a small project", "Mentor a junior developer"]
                }
        
        return Command(
            goto="resources_agent",
            update={
                "learning_path": learning_data,
                "messages": state["messages"] + [response]
            }
        ) 