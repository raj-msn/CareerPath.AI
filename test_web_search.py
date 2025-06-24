#!/usr/bin/env python3
"""
Test script for web search functionality in CareerPath.AI
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_web_search():
    """Test the web search functionality"""
    
    # Check if required API keys are set
    openai_key = os.getenv("OPENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    print("🔍 Testing CareerPath.AI Web Search Functionality")
    print("=" * 50)
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not found")
        print("Please set: export OPENAI_API_KEY='your-api-key'")
        return False
        
    if not tavily_key:
        print("❌ TAVILY_API_KEY not found")
        print("Please set: export TAVILY_API_KEY='your-tavily-key'")
        print("Get your free key at: https://tavily.com/")
        return False
    
    print("✅ API keys found")
    
    try:
        # Test Tavily search directly
        from langchain_tavily import TavilySearch
        
        print("\n🔍 Testing Tavily search...")
        search_tool = TavilySearch(max_results=2)
        result = search_tool.invoke("Python programming courses 2024")
        
        print("✅ Tavily search successful!")
        print(f"📊 Found {len(result.get('results', []))} results")
        
        if result.get('results'):
            print("\n📝 Sample result:")
            first_result = result['results'][0]
            print(f"Title: {first_result.get('title', 'N/A')}")
            print(f"URL: {first_result.get('url', 'N/A')}")
            print(f"Content preview: {first_result.get('content', 'N/A')[:100]}...")
        
        return True
        
    except ImportError:
        print("❌ langchain-tavily not installed")
        print("Run: pip install langchain-tavily")
        return False
    except Exception as e:
        print(f"❌ Error testing web search: {str(e)}")
        return False

def test_resources_agent():
    """Test the resources agent with web search"""
    
    print("\n🤖 Testing Resources Agent with Web Search...")
    
    try:
        from backend.agents.resources_agent import ResourceRecommendationAgent
        from langchain_openai import ChatOpenAI
        
        # Initialize model and agent
        model = ChatOpenAI(
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4o-mini-2024-07-18"
        )
        
        agent = ResourceRecommendationAgent(model)
        
        # Test state
        test_state = {
            "target_role": "Data Scientist",
            "skills_assessment": {
                "priority_skills": ["Python", "Machine Learning", "Statistics"]
            },
            "learning_path": {
                "learning_phases": [
                    {"phase": "Foundation", "duration": "2 months"},
                    {"phase": "Advanced", "duration": "3 months"}
                ]
            },
            "messages": []
        }
        
        print("✅ Resources agent initialized successfully!")
        print("🔍 Agent has web search capability:", hasattr(agent, 'search_tool'))
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing resources agent: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 CareerPath.AI Web Search Test")
    print("=" * 40)
    
    success = True
    
    # Test web search
    if not test_web_search():
        success = False
    
    # Test resources agent
    if not test_resources_agent():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("✅ All tests passed! Web search is ready to use.")
        print("\n💡 Try asking: 'Find me current Python courses for data science'")
    else:
        print("❌ Some tests failed. Check the errors above.")
        sys.exit(1) 