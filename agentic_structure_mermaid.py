#!/usr/bin/env python3
"""
CareerPath.AI Agentic Structure - Mermaid Diagrams

This script generates Mermaid diagrams for the multi-agent system architecture
that can be easily viewed in GitHub, documentation, or Mermaid Live Editor.
"""

def generate_agent_workflow_mermaid():
    """Generate Mermaid flowchart for the agent workflow"""
    
    mermaid_code = """
graph TD
    %% User Interface Layer
    User[👤 User Input<br/>Career Query] --> Supervisor[🎯 Supervisor Agent<br/>Orchestrator]
    
    %% Agent Layer
    Supervisor --> Skills[📊 Skills Assessment<br/>Agent]
    Supervisor --> Industry[🏢 Industry Research<br/>Agent]
    Supervisor --> Learning[🛤️ Learning Path<br/>Agent]
    Supervisor --> Resources[📚 Resources Agent<br/>+ Web Search]
    
    %% External Tools
    Skills --> GPT[🤖 GPT-4o-mini<br/>LLM]
    Industry --> GPT
    Learning --> GPT
    Resources --> GPT
    Resources --> Tavily[🔍 Tavily<br/>Web Search API]
    
    %% State Management
    Skills --> State[💾 Shared State<br/>LangGraph]
    Industry --> State
    Learning --> State
    Resources --> State
    
    %% Output Layer
    State --> Frontend[⚛️ React Frontend<br/>Chat Interface]
    State --> ReactFlow[🗺️ React Flow<br/>Interactive Roadmap]
    State --> Links[🔗 Clickable Links<br/>Courses & Certs]
    State --> API[🚀 FastAPI<br/>Backend Server]
    
    %% Styling
    classDef userLayer fill:#E3F2FD,stroke:#1976D2,stroke-width:2px
    classDef supervisorLayer fill:#FFF3E0,stroke:#F57C00,stroke-width:2px
    classDef agentLayer fill:#E8F5E8,stroke:#388E3C,stroke-width:2px
    classDef toolLayer fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
    classDef stateLayer fill:#FAFAFA,stroke:#616161,stroke-width:2px
    classDef outputLayer fill:#FFF8E1,stroke:#F9A825,stroke-width:2px
    
    class User userLayer
    class Supervisor supervisorLayer
    class Skills,Industry,Learning,Resources agentLayer
    class GPT,Tavily toolLayer
    class State stateLayer
    class Frontend,ReactFlow,Links,API outputLayer
    """
    
    return mermaid_code.strip()

def generate_data_flow_mermaid():
    """Generate Mermaid diagram for data flow"""
    
    mermaid_code = """
graph LR
    %% Input Data
    Query[📝 User Query<br/>"I want to become<br/>a senior engineer"] --> Processing{🔄 Agent Processing}
    
    %% Agent Data Processing
    Processing --> SkillsData[📊 Skills Analysis<br/>strengths, gaps, level]
    Processing --> IndustryData[🏢 Industry Research<br/>salary, demand, trends]
    Processing --> LearningData[🛤️ Learning Path<br/>phases, timeline, milestones]
    Processing --> ResourcesData[📚 Resources Collection<br/>courses, certifications]
    
    %% Web Search Enhancement
    ResourcesData --> WebSearch[🔍 Web Search<br/>Tavily API]
    WebSearch --> CurrentResources[📋 Current Resources<br/>up-to-date links]
    
    %% State Aggregation
    SkillsData --> SharedState[💾 CareerPlanningState<br/>LangGraph]
    IndustryData --> SharedState
    LearningData --> SharedState
    CurrentResources --> SharedState
    
    %% Output Generation
    SharedState --> JSONResponse[📤 JSON Response<br/>structured data]
    SharedState --> ChatResponse[💬 Chat Response<br/>markdown text]
    SharedState --> FlowData[🗺️ Flow Data<br/>nodes & edges]
    
    %% Frontend Rendering
    JSONResponse --> ReactApp[⚛️ React App]
    ChatResponse --> ChatUI[💬 Chat Interface]
    FlowData --> Visualization[🗺️ Interactive Roadmap]
    
    %% User Interaction
    Visualization --> ClickableLinks[🔗 Clickable Resources<br/>direct access to courses]
    
    %% Styling
    classDef inputData fill:#E3F2FD,stroke:#1976D2
    classDef processing fill:#FFF3E0,stroke:#F57C00
    classDef agentData fill:#E8F5E8,stroke:#388E3C
    classDef webData fill:#F3E5F5,stroke:#7B1FA2
    classDef stateData fill:#FAFAFA,stroke:#616161
    classDef outputData fill:#FFF8E1,stroke:#F9A825
    classDef uiData fill:#E1F5FE,stroke:#0277BD
    
    class Query inputData
    class Processing processing
    class SkillsData,IndustryData,LearningData,ResourcesData agentData
    class WebSearch,CurrentResources webData
    class SharedState stateData
    class JSONResponse,ChatResponse,FlowData outputData
    class ReactApp,ChatUI,Visualization,ClickableLinks uiData
    """
    
    return mermaid_code.strip()

def generate_system_architecture_mermaid():
    """Generate high-level system architecture diagram"""
    
    mermaid_code = """
graph TB
    subgraph "Frontend Layer"
        React[React Application]
        Chat[Chat Interface]
        Flow[React Flow Visualization]
        Links[Resource Links]
    end
    
    subgraph "API Layer"
        FastAPI[FastAPI Server]
        Endpoints[REST Endpoints]
    end
    
    subgraph "Agent Layer"
        Supervisor[Supervisor Agent]
        Skills[Skills Agent]
        Industry[Industry Agent]
        Learning[Learning Agent]
        Resources[Resources Agent]
    end
    
    subgraph "State Management"
        LangGraph[LangGraph State]
        Memory[Conversation Memory]
    end
    
    subgraph "External Services"
        OpenAI[GPT-4o-mini API]
        Tavily[Tavily Search API]
    end
    
    %% Connections
    React --> FastAPI
    Chat --> FastAPI
    Flow --> FastAPI
    Links --> FastAPI
    
    FastAPI --> Endpoints
    Endpoints --> Supervisor
    
    Supervisor --> Skills
    Supervisor --> Industry
    Supervisor --> Learning
    Supervisor --> Resources
    
    Skills --> LangGraph
    Industry --> LangGraph
    Learning --> LangGraph
    Resources --> LangGraph
    
    LangGraph --> Memory
    
    Skills --> OpenAI
    Industry --> OpenAI
    Learning --> OpenAI
    Resources --> OpenAI
    Resources --> Tavily
    
    %% Styling
    classDef frontend fill:#E3F2FD,stroke:#1976D2,stroke-width:2px
    classDef api fill:#FFF3E0,stroke:#F57C00,stroke-width:2px
    classDef agents fill:#E8F5E8,stroke:#388E3C,stroke-width:2px
    classDef state fill:#FAFAFA,stroke:#616161,stroke-width:2px
    classDef external fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
    
    class React,Chat,Flow,Links frontend
    class FastAPI,Endpoints api
    class Supervisor,Skills,Industry,Learning,Resources agents
    class LangGraph,Memory state
    class OpenAI,Tavily external
    """
    
    return mermaid_code.strip()

def save_mermaid_diagrams():
    """Generate and save all Mermaid diagrams to files"""
    
    print("🎨 Generating Mermaid Diagrams for CareerPath.AI Architecture...")
    
    # Agent Workflow Diagram
    workflow_diagram = generate_agent_workflow_mermaid()
    with open('agent_workflow.mmd', 'w') as f:
        f.write(workflow_diagram)
    print("✅ Saved: agent_workflow.mmd")
    
    # Data Flow Diagram
    dataflow_diagram = generate_data_flow_mermaid()
    with open('data_flow.mmd', 'w') as f:
        f.write(dataflow_diagram)
    print("✅ Saved: data_flow.mmd")
    
    # System Architecture Diagram
    architecture_diagram = generate_system_architecture_mermaid()
    with open('system_architecture.mmd', 'w') as f:
        f.write(architecture_diagram)
    print("✅ Saved: system_architecture.mmd")
    
    # Create a combined README with all diagrams
    readme_content = f"""
# CareerPath.AI - Agentic Architecture Diagrams

This directory contains visual representations of the CareerPath.AI multi-agent system architecture.

## 1. Agent Workflow Diagram

Shows the complete workflow from user input to final output through the multi-agent system.

```mermaid
{workflow_diagram}
```

## 2. Data Flow Diagram

Illustrates how data flows through the system from query to response.

```mermaid
{dataflow_diagram}
```

## 3. System Architecture Diagram

High-level view of the system components and their relationships.

```mermaid
{architecture_diagram}
```

## Usage

1. **View in GitHub**: These Mermaid diagrams will render automatically in GitHub markdown files
2. **Mermaid Live Editor**: Copy the diagram code to [Mermaid Live](https://mermaid.live/) for editing
3. **Documentation**: Embed these diagrams in your project documentation
4. **Export**: Use Mermaid CLI or online tools to export as PNG/SVG

## Key Components

- **Supervisor Agent**: Orchestrates the entire workflow
- **Specialized Agents**: Skills, Industry, Learning Path, Resources
- **External APIs**: GPT-4o-mini for LLM capabilities, Tavily for web search
- **State Management**: LangGraph handles shared state between agents
- **Frontend**: React with interactive visualization using React Flow
- **Real-time Search**: Tavily integration for current learning resources

## Architecture Benefits

1. **Modularity**: Each agent has a specific responsibility
2. **Scalability**: Easy to add new agents or modify existing ones
3. **State Management**: Centralized state through LangGraph
4. **Real-time Data**: Web search integration for current information
5. **Interactive UI**: Visual career roadmap with clickable resources
"""
    
    with open('ARCHITECTURE_DIAGRAMS.md', 'w') as f:
        f.write(readme_content.strip())
    print("✅ Saved: ARCHITECTURE_DIAGRAMS.md")
    
    print("\n📊 Mermaid diagrams generated successfully!")
    print("🔍 Files created:")
    print("   - agent_workflow.mmd (Agent workflow)")
    print("   - data_flow.mmd (Data flow)")
    print("   - system_architecture.mmd (System architecture)")
    print("   - ARCHITECTURE_DIAGRAMS.md (Combined documentation)")
    print("\n💡 Tip: View these diagrams in GitHub or paste into Mermaid Live Editor!")

if __name__ == "__main__":
    save_mermaid_diagrams() 