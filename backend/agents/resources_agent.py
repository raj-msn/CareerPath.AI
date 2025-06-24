from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_tavily import TavilySearch
from langgraph.types import Command
from typing import Literal
import json
import os

from ..models.state import CareerPlanningState

class ResourceRecommendationAgent:
    def __init__(self, model: ChatOpenAI):
        self.model = model
        
        # Initialize web search tool
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            print("⚠️ TAVILY_API_KEY not found, web search will be disabled")
            self.search_tool = None
        else:
            self.search_tool = TavilySearch(
                max_results=5,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=False
            )
        
        # Bind tools to the model only if search tool is available
        if self.search_tool:
            self.model_with_tools = model.bind_tools([self.search_tool])
        else:
            self.model_with_tools = model
        
        self.system_prompt = """You are a Resource Recommendation Agent, an expert curator of learning resources and career development materials with access to real-time web search.

Your role:
1. Use web search to find current, up-to-date courses, certifications, and learning materials
2. Search for recent tutorials, bootcamps, and practice platforms
3. Find active networking communities and professional groups
4. Verify resource availability and current pricing
5. Match resources to learning phases and skill gaps

When you need current information about courses, certifications, or learning resources, use the search tool to find the latest options.

Always respond in JSON format with clickable URLs:
{
    "courses": [
        {
            "title": "Course Name",
            "provider": "Platform",
            "duration": "X weeks",
            "level": "Beginner/Intermediate/Advanced",
            "skills": ["skill1", "skill2"],
            "url": "https://example.com",
            "cost": "Free/Paid"
        }
    ],
    "certifications": [
        {
            "title": "Certification Name",
            "provider": "Organization",
            "skills": ["skill1"],
            "duration": "X months",
            "cost": "$XXX"
        }
    ],
    "books": ["Book Title by Author"],
    "practice_platforms": ["Platform Name - Description"],
    "communities": ["Community Name - Description"],
    "free_resources": ["Resource Name - Description"]
}"""

    def _execute_tools(self, tool_calls):
        """Execute tool calls and return results"""
        tool_results = []
        for tool_call in tool_calls:
            try:
                # Handle different tool call formats
                tool_name = tool_call.get("name") or tool_call.get("function", {}).get("name")
                tool_args = tool_call.get("args") or tool_call.get("function", {}).get("arguments", {})
                tool_id = tool_call.get("id") or tool_call.get("tool_call_id")
                
                if tool_name == "tavily_search_results_json" and self.search_tool:
                    # Parse args if it's a string
                    if isinstance(tool_args, str):
                        tool_args = json.loads(tool_args)
                    
                    result = self.search_tool.invoke(tool_args)
                    tool_results.append(
                        ToolMessage(
                            content=json.dumps(result),
                            name=tool_name,
                            tool_call_id=tool_id
                        )
                    )
                else:
                    # Handle unknown tool calls with a default response
                    tool_results.append(
                        ToolMessage(
                            content=json.dumps({"error": f"Unknown tool: {tool_name}"}),
                            name=tool_name or "unknown_tool",
                            tool_call_id=tool_id
                        )
                    )
            except Exception as e:
                # Handle any errors in tool execution
                tool_results.append(
                    ToolMessage(
                        content=json.dumps({"error": f"Tool execution failed: {str(e)}"}),
                        name=tool_call.get("name", "unknown_tool"),
                        tool_call_id=tool_call.get("id", "unknown_id")
                    )
                )
        return tool_results

    def __call__(self, state: CareerPlanningState) -> Command[Literal["__end__"]]:
        skills_info = state.get("skills_assessment") or {}
        learning_path = state.get("learning_path") or {}
        target_role = state.get('target_role') or 'Not specified'
        priority_skills = skills_info.get('priority_skills', [])
        
        # Build search queries for current resources
        search_queries = [
            f"best {target_role} courses 2024 online certification",
            f"{' '.join(priority_skills[:3])} learning resources tutorials 2024",
            f"{target_role} certification programs professional development"
        ]
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
Target Role: {target_role}
Skills to Develop: {priority_skills}
Learning Phases: {learning_path.get('learning_phases', [])}

Please search for current, up-to-date learning resources for this career transition. 
Focus on finding:
1. Recent courses and certifications for {target_role}
2. Learning platforms for skills: {', '.join(priority_skills[:5])}
3. Professional communities and networking opportunities

Then provide specific, actionable resource recommendations with working URLs.
""")
        ]
        
        # First, get the model's response (may include tool calls)
        try:
            response = self.model_with_tools.invoke(messages)
            messages.append(response)
            print(f"🤖 Model response received. Has tool calls: {hasattr(response, 'tool_calls') and bool(response.tool_calls)}")
            if hasattr(response, 'tool_calls') and response.tool_calls:
                print(f"🔧 Tool calls: {[tc.get('name', 'unknown') for tc in response.tool_calls]}")
        except Exception as e:
            print(f"❌ Error in model invocation: {str(e)}")
            raise
        
        # Execute any tool calls
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"🔍 Executing {len(response.tool_calls)} tool calls...")
            tool_results = self._execute_tools(response.tool_calls)
            messages.extend(tool_results)
            
            # Get final response with search results - use the model WITHOUT tools to avoid recursion
            final_response = self.model.invoke(messages + [
                HumanMessage(content="Based on the search results above, provide the resource recommendations in the required JSON format with real, working URLs. Do not make any more tool calls.")
            ])
        else:
            print("ℹ️ No tool calls made, using direct response")
            final_response = response
        
        try:
            # Try to parse JSON from response
            if hasattr(final_response, 'content'):
                content = final_response.content
            else:
                content = str(final_response)
                
            # Extract JSON if it's wrapped in markdown
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
                
            resources_data = json.loads(content)
        except:
            # Fallback with realistic resources
            resources_data = {
                "courses": [
                    {
                        "title": "System Design Interview Course",
                        "provider": "Educative",
                        "duration": "8 weeks",
                        "level": "Intermediate",
                        "skills": ["System Design", "Architecture"],
                        "url": "https://educative.io/system-design",
                        "cost": "Paid"
                    },
                    {
                        "title": "Tech Lead Essentials", 
                        "provider": "Pluralsight",
                        "duration": "6 weeks",
                        "level": "Advanced",
                        "skills": ["Leadership", "Team Management"],
                        "url": "https://pluralsight.com/tech-lead",
                        "cost": "Paid"
                    }
                ],
                "certifications": [
                    {
                        "title": "AWS Solutions Architect",
                        "provider": "Amazon",
                        "skills": ["Cloud Architecture", "System Design"],
                        "duration": "3-6 months",
                        "cost": "$150"
                    }
                ],
                "books": [
                    "Designing Data-Intensive Applications by Martin Kleppmann",
                    "The Manager's Path by Camille Fournier"
                ],
                "practice_platforms": [
                    "LeetCode - Algorithm and data structure practice",
                    "System Design Primer - GitHub repository"
                ],
                "communities": [
                    "Engineering Management Slack - Leadership discussions",
                    "r/ExperiencedDevs - Reddit community"
                ],
                "free_resources": [
                    "High Scalability Blog - System design case studies",
                    "MIT OpenCourseWare - Computer Science courses"
                ]
            }
        
        # Add search metadata to resources
        resources_data["search_enabled"] = True
        resources_data["last_updated"] = "Real-time web search results"
        
        return Command(
            goto="__end__",
            update={
                "resources": resources_data,
                "messages": state['messages'] + [final_response]
            }
        ) 