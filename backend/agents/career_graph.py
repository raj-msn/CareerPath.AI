import os
from typing import Literal
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.constants import START
from langchain.schema import HumanMessage

from .supervisor import CareerSupervisorAgent
from .skills_agent import SkillsAssessmentAgent
from .industry_agent import IndustryResearchAgent
from .learning_agent import LearningPathAgent
from .resources_agent import ResourceRecommendationAgent
from ..models.state import CareerPlanningState

class CareerPlanningGraph:
    def __init__(self, openai_api_key: str):
        # Initialize the LLM
        self.model = ChatOpenAI(
            temperature=0.1,
            api_key=openai_api_key,
            model="gpt-4o-mini-2024-07-18"
        )
        
        # Initialize all agents
        self.supervisor = CareerSupervisorAgent(self.model)
        self.skills_agent = SkillsAssessmentAgent(self.model)
        self.industry_agent = IndustryResearchAgent(self.model)
        self.learning_agent = LearningPathAgent(self.model)
        self.resources_agent = ResourceRecommendationAgent(self.model)
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph multi-agent workflow"""
        
        # Create the graph builder
        builder = StateGraph(CareerPlanningState)
        
        # Add all agent nodes
        builder.add_node("supervisor", self.supervisor)
        builder.add_node("skills_agent", self.skills_agent)
        builder.add_node("industry_agent", self.industry_agent)
        builder.add_node("learning_agent", self.learning_agent)
        builder.add_node("resources_agent", self.resources_agent)
        
        # Define the workflow entry point
        builder.set_entry_point("supervisor")
        
        # All agents return to supervisor except resources_agent (which ends)
        # The Command objects in each agent handle the routing
        
        return builder.compile()
    
    def plan_career(self, user_message: str, current_role: str = None, target_role: str = None, 
                   conversation_history: list = None, existing_learning_path: dict = None, 
                   is_follow_up: bool = False):
        """Enhanced career planning with conversation context"""
        
        # Create initial state with context
        initial_state = {
            "messages": [HumanMessage(content=user_message)],
            "current_role": current_role,
            "target_role": target_role,
            "conversation_history": conversation_history or [],
            "existing_learning_path": existing_learning_path,
            "is_follow_up": is_follow_up
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        # Extract the final response
        return {
            "message": self._generate_summary(result, is_follow_up),
            "mermaid_chart": result.get("mermaid_chart", ""),
            "skills_assessment": result.get("skills_assessment", {}),
            "industry_insights": result.get("industry_insights", {}),
            "learning_path": result.get("learning_path", {}),
            "resources": result.get("resources", {}),
            "current_role": result.get("current_role"),
            "target_role": result.get("target_role"),
            "is_follow_up": is_follow_up
        }
    
    def _generate_summary(self, result, is_follow_up=False):
        """Generate a comprehensive summary from all agent outputs"""
        
        summary_parts = []
        
        # Different intro for follow-ups vs new plans
        if is_follow_up:
            summary_parts.append(f"## 🔄 Updated Career Plan\n")
            summary_parts.append(f"Based on your follow-up question, I've refined your career roadmap:\n")
        else:
            # Career transition overview with proper markdown
            if result.get("current_role") and result.get("target_role"):
                summary_parts.append(f"# 🎯 Career Transition Plan\n**{result['current_role']} → {result['target_role']}**\n")
        
        # Skills assessment summary
        skills = result.get("skills_assessment", {})
        if skills:
            summary_parts.append(f"## 📊 Skills Analysis\n")
            if skills.get("skill_gaps"):
                gap_list = "\n".join([f"• {skill}" for skill in skills['skill_gaps'][:5]])
                summary_parts.append(f"**Key skills to develop:**\n{gap_list}\n")
            if skills.get("strengths"):
                strength_list = "\n".join([f"• {skill}" for skill in skills['strengths'][:5]])
                summary_parts.append(f"**Your strengths:**\n{strength_list}\n")
        
        # Industry insights
        industry = result.get("industry_insights", {})
        if industry:
            summary_parts.append(f"## 🏢 Industry Outlook\n")
            summary_parts.append(f"**Market demand:** {industry.get('market_demand', 'Good opportunities')}\n")
            if industry.get("salary_range"):
                salary = industry["salary_range"]
                summary_parts.append(f"**Salary range:** ${salary.get('min', 'N/A'):,} - ${salary.get('max', 'N/A'):,} {salary.get('currency', 'USD')}\n")
            if industry.get("growth_projection"):
                summary_parts.append(f"**Growth projection:** {industry['growth_projection']}\n")
        
        # Learning path
        learning = result.get("learning_path", {})
        if learning:
            if is_follow_up:
                summary_parts.append(f"## 📚 Refined Learning Path\n")
            else:
                summary_parts.append(f"## 📚 Learning Roadmap\n")
            
            summary_parts.append(f"**Timeline:** {learning.get('timeline', '6-12 months')}\n")
            if learning.get("learning_phases"):
                summary_parts.append(f"**Key phases:**\n")
                for i, phase in enumerate(learning["learning_phases"][:4], 1):
                    phase_name = phase.get("phase", f"Phase {i}")
                    duration = phase.get("duration", "X months")
                    summary_parts.append(f"{i}. **{phase_name}** _{duration}_")
                summary_parts.append("")  # Add blank line
        
        # Resources with clickable links
        resources = result.get("resources", {})
        if resources:
            summary_parts.append(f"## 🎓 Recommended Resources")
            
            # Add search indicator if web search was used
            if resources.get("search_enabled"):
                summary_parts.append(f"_✨ Real-time web search results included_\n")
            
            # Top courses with links
            if resources.get("courses"):
                summary_parts.append(f"### 📖 Courses")
                for course in resources["courses"][:3]:  # Show top 3
                    title = course.get("title", "Course")
                    provider = course.get("provider", "Provider")
                    level = course.get("level", "")
                    duration = course.get("duration", "")
                    url = course.get("url", "")
                    cost = course.get("cost", "")
                    
                    course_line = f"• **[{title}]({url})** by {provider}"
                    if level or duration or cost:
                        details = " • ".join(filter(None, [level, duration, cost]))
                        course_line += f" _{details}_"
                    summary_parts.append(course_line)
                summary_parts.append("")
            
            # Certifications with links
            if resources.get("certifications"):
                summary_parts.append(f"### 🏆 Certifications")
                for cert in resources["certifications"][:2]:  # Show top 2
                    title = cert.get("title", "Certification")
                    provider = cert.get("provider", "Provider")
                    cost = cert.get("cost", "")
                    duration = cert.get("duration", "")
                    
                    cert_line = f"• **{title}** by {provider}"
                    if cost or duration:
                        details = " • ".join(filter(None, [duration, cost]))
                        cert_line += f" _{details}_"
                    summary_parts.append(cert_line)
                summary_parts.append("")
            
            # Practice platforms with descriptions
            if resources.get("practice_platforms"):
                summary_parts.append(f"### 💻 Practice Platforms")
                for platform in resources["practice_platforms"][:3]:
                    summary_parts.append(f"• {platform}")
                summary_parts.append("")
            
            # Communities
            if resources.get("communities"):
                summary_parts.append(f"### 👥 Communities")
                for community in resources["communities"][:2]:
                    summary_parts.append(f"• {community}")
                summary_parts.append("")
        
        # Call to action - different for follow-ups
        summary_parts.append(f"---\n")
        if is_follow_up:
            summary_parts.append(f"✨ **Your career roadmap has been updated!** Check the refined timeline on the interactive chart.\n")
        else:
            summary_parts.append(f"✨ **Your personalized career roadmap is ready!** Check the visual timeline on the right panel.\n")
        
        return "\n".join(summary_parts)

# Factory function for easy instantiation
def create_career_planning_graph(openai_api_key: str = None):
    """Create a CareerPlanningGraph instance"""
    if not openai_api_key:
        openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        raise ValueError("OpenAI API key is required")
    
    return CareerPlanningGraph(openai_api_key) 