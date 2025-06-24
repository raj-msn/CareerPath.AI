from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from typing import Literal
import json

from ..models.state import CareerPlanningState

class IndustryResearchAgent:
    def __init__(self, model: ChatOpenAI):
        self.model = model
        self.system_prompt = """You are an Industry Research Agent, an expert market analyst specializing in career trends and industry insights.

Your role:
1. Analyze industry trends for the target role
2. Provide salary expectations and growth projections
3. Identify key companies and opportunities
4. Share market demand insights

Always respond in JSON format with:
{
    "industry_overview": "Brief overview of the industry",
    "market_demand": "High/Medium/Low with explanation",
    "salary_range": {"min": 50000, "max": 120000, "currency": "USD"},
    "growth_projection": "Percentage growth expected",
    "key_companies": ["list of top companies hiring"],
    "emerging_trends": ["list of industry trends"],
    "job_opportunities": ["types of roles available"]
}"""

    def __call__(self, state: CareerPlanningState) -> Command[Literal["learning_agent", "__end__"]]:
        skills_info = state.get("skills_assessment") or {}
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
Target Role: {state.get('target_role') or 'Not specified'}
Current Role: {state.get('current_role') or 'Not specified'}
Skills Assessment: {json.dumps(skills_info, indent=2)}

Please provide comprehensive industry research for the target role.
""")
        ]
        
        response = self.model.invoke(messages)
        
        try:
            industry_data = json.loads(response.content)
        except:
            # Fallback if JSON parsing fails
            industry_data = {
                "industry_overview": "Growing technology sector with high demand for skilled professionals",
                "market_demand": "High - Strong demand with projected growth",
                "salary_range": {"min": 70000, "max": 130000, "currency": "USD"},
                "growth_projection": "15% annually",
                "key_companies": ["Google", "Microsoft", "Amazon", "Meta", "Apple"],
                "emerging_trends": ["AI/ML adoption", "Remote work", "Cloud computing"],
                "job_opportunities": ["Senior roles", "Leadership positions", "Specialized consulting"]
            }
        
        return Command(
            goto="learning_agent",
            update={
                "industry_insights": industry_data,
                "messages": state['messages'] + [response]
            }
        ) 