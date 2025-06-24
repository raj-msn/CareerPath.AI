from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from typing import Literal
import json

from ..models.state import CareerPlanningState

class SkillsAssessmentAgent:
    def __init__(self, model: ChatOpenAI):
        self.model = model
        self.system_prompt = """You are a Skills Assessment Agent, an expert career mentor specializing in skill gap analysis.

Your role:
1. Analyze the user's current role and skills
2. Compare with target role requirements
3. Identify skill gaps and strengths
4. Provide actionable skill development recommendations

Always respond in JSON format with:
{
    "current_skills": ["list of identified current skills"],
    "required_skills": ["list of skills needed for target role"],
    "skill_gaps": ["list of missing skills"],
    "strengths": ["list of transferable skills"],
    "priority_skills": ["top 3-5 skills to focus on first"]
}"""

    def __call__(self, state: CareerPlanningState) -> Command[Literal["industry_agent", "__end__"]]:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
Current Role: {state.get('current_role') or 'Not specified'}
Target Role: {state.get('target_role') or 'Not specified'}
User Query: {state['messages'][-1].content if state.get('messages') else 'No query'}

Please assess the skills gap between current and target roles.
""")
        ]
        
        response = self.model.invoke(messages)
        
        try:
            skills_data = json.loads(response.content)
        except:
            # Fallback if JSON parsing fails
            skills_data = {
                "current_skills": ["Basic programming", "Communication"],
                "required_skills": ["Advanced programming", "Leadership", "Data analysis"],
                "skill_gaps": ["Leadership", "Data analysis"],
                "strengths": ["Communication", "Problem solving"],
                "priority_skills": ["Leadership", "Data analysis", "Project management"]
            }
        
        return Command(
            goto="industry_agent",
            update={
                "skills_assessment": skills_data,
                "messages": state['messages'] + [response]
            }
        ) 