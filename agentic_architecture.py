#!/usr/bin/env python3
"""
CareerPath.AI Agentic Architecture Visualizer

This script generates a visual diagram of the multi-agent system architecture
showing the workflow, data flow, and interactions between agents.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_agentic_diagram():
    """Create a comprehensive diagram of the CareerPath.AI agentic architecture"""
    
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define colors for different components
    colors = {
        'user': '#E3F2FD',           # Light blue
        'supervisor': '#FFF3E0',      # Light orange
        'agents': '#E8F5E8',         # Light green
        'tools': '#F3E5F5',          # Light purple
        'output': '#FFF8E1',         # Light yellow
        'data': '#FAFAFA'            # Light gray
    }
    
    # Define agent positions and sizes
    agents = {
        'user_input': {'pos': (1, 8.5), 'size': (1.5, 0.8), 'color': colors['user'], 'label': '👤 User Input\n(Career Query)'},
        'supervisor': {'pos': (4.5, 8.5), 'size': (2, 0.8), 'color': colors['supervisor'], 'label': '🎯 Supervisor Agent\n(Orchestrator)'},
        'skills': {'pos': (1, 6.5), 'size': (1.8, 0.8), 'color': colors['agents'], 'label': '📊 Skills Assessment\nAgent'},
        'industry': {'pos': (3.2, 6.5), 'size': (1.8, 0.8), 'color': colors['agents'], 'label': '🏢 Industry Research\nAgent'},
        'learning': {'pos': (5.4, 6.5), 'size': (1.8, 0.8), 'color': colors['agents'], 'label': '🛤️ Learning Path\nAgent'},
        'resources': {'pos': (7.6, 6.5), 'size': (1.8, 0.8), 'color': colors['agents'], 'label': '📚 Resources Agent\n(+ Web Search)'},
        'web_search': {'pos': (8.5, 4.5), 'size': (1.2, 0.6), 'color': colors['tools'], 'label': '🔍 Tavily\nWeb Search'},
        'openai': {'pos': (1, 4.5), 'size': (1.2, 0.6), 'color': colors['tools'], 'label': '🤖 GPT-4o-mini\nLLM'},
        'state': {'pos': (4.5, 4.5), 'size': (2, 0.8), 'color': colors['data'], 'label': '💾 Shared State\n(LangGraph)'},
        'frontend': {'pos': (1, 2.5), 'size': (1.8, 0.8), 'color': colors['output'], 'label': '⚛️ React Frontend\n(Chat + Visualization)'},
        'react_flow': {'pos': (3.2, 2.5), 'size': (1.8, 0.8), 'color': colors['output'], 'label': '🗺️ React Flow\n(Interactive Roadmap)'},
        'resources_ui': {'pos': (5.4, 2.5), 'size': (1.8, 0.8), 'color': colors['output'], 'label': '🔗 Clickable Links\n(Courses & Certs)'},
        'api': {'pos': (7.6, 2.5), 'size': (1.8, 0.8), 'color': colors['output'], 'label': '🚀 FastAPI\n(Backend Server)'}
    }
    
    # Draw agent boxes
    for agent_id, config in agents.items():
        x, y = config['pos']
        w, h = config['size']
        
        # Create rounded rectangle
        box = FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.05",
            facecolor=config['color'],
            edgecolor='gray',
            linewidth=1.5
        )
        ax.add_patch(box)
        
        # Add text
        ax.text(x, y, config['label'], 
               ha='center', va='center', 
               fontsize=9, fontweight='bold',
               wrap=True)
    
    # Define workflow arrows
    arrows = [
        # Main workflow
        ('user_input', 'supervisor', 'User Query'),
        ('supervisor', 'skills', 'Analyze Skills'),
        ('supervisor', 'industry', 'Research Market'),
        ('supervisor', 'learning', 'Create Path'),
        ('supervisor', 'resources', 'Find Resources'),
        
        # Tool connections
        ('resources', 'web_search', 'Search API'),
        ('skills', 'openai', 'LLM Call'),
        ('industry', 'openai', ''),
        ('learning', 'openai', ''),
        ('resources', 'openai', ''),
        
        # State management
        ('skills', 'state', 'Update'),
        ('industry', 'state', ''),
        ('learning', 'state', ''),
        ('resources', 'state', ''),
        
        # Output flow
        ('state', 'frontend', 'Response'),
        ('state', 'react_flow', 'Learning Path'),
        ('state', 'resources_ui', 'Resources'),
        ('state', 'api', 'JSON Data')
    ]
    
    # Draw arrows
    for start, end, label in arrows:
        start_pos = agents[start]['pos']
        end_pos = agents[end]['pos']
        
        # Calculate arrow positions
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        # Adjust start and end points to box edges
        start_w, start_h = agents[start]['size']
        end_w, end_h = agents[end]['size']
        
        if abs(dx) > abs(dy):  # Horizontal arrow
            if dx > 0:  # Right
                arrow_start = (start_pos[0] + start_w/2, start_pos[1])
                arrow_end = (end_pos[0] - end_w/2, end_pos[1])
            else:  # Left
                arrow_start = (start_pos[0] - start_w/2, start_pos[1])
                arrow_end = (end_pos[0] + end_w/2, end_pos[1])
        else:  # Vertical arrow
            if dy > 0:  # Up
                arrow_start = (start_pos[0], start_pos[1] + start_h/2)
                arrow_end = (end_pos[0], end_pos[1] - end_h/2)
            else:  # Down
                arrow_start = (start_pos[0], start_pos[1] - start_h/2)
                arrow_end = (end_pos[0], end_pos[1] + end_h/2)
        
        # Draw arrow
        arrow = ConnectionPatch(
            arrow_start, arrow_end, "data", "data",
            arrowstyle="->", shrinkA=5, shrinkB=5,
            mutation_scale=15, fc="darkblue", alpha=0.7
        )
        ax.add_patch(arrow)
        
        # Add label if provided
        if label:
            mid_x = (arrow_start[0] + arrow_end[0]) / 2
            mid_y = (arrow_start[1] + arrow_end[1]) / 2
            ax.text(mid_x, mid_y, label, 
                   ha='center', va='center', 
                   fontsize=7, style='italic',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # Add title and legend
    ax.text(5, 9.5, 'CareerPath.AI - Multi-Agent Architecture', 
           ha='center', va='center', fontsize=18, fontweight='bold')
    
    # Create legend
    legend_elements = [
        mpatches.Patch(color=colors['user'], label='User Interface'),
        mpatches.Patch(color=colors['supervisor'], label='Supervisor Agent'),
        mpatches.Patch(color=colors['agents'], label='Specialized Agents'),
        mpatches.Patch(color=colors['tools'], label='External Tools/APIs'),
        mpatches.Patch(color=colors['data'], label='State Management'),
        mpatches.Patch(color=colors['output'], label='Output Components')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    # Add workflow description
    workflow_text = """
    Workflow:
    1. User submits career query
    2. Supervisor orchestrates agent execution
    3. Agents analyze skills, research industry, create learning path
    4. Resources agent searches web for current materials
    5. Results compiled and sent to React frontend
    6. Interactive roadmap with clickable links displayed
    """
    
    ax.text(0.5, 1, workflow_text, 
           ha='left', va='bottom', fontsize=10,
           bbox=dict(boxstyle="round,pad=0.5", facecolor='#F5F5F5', alpha=0.9))
    
    plt.tight_layout()
    return fig

def create_data_flow_diagram():
    """Create a detailed data flow diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Data structures and their flow
    data_boxes = {
        'user_query': {'pos': (1, 7), 'size': (1.5, 0.6), 'label': '📝 User Query\n"I want to become\na senior engineer"'},
        'skills_data': {'pos': (1, 5.5), 'size': (1.5, 0.8), 'label': '📊 Skills Data\n{\n  "strengths": [...],\n  "gaps": [...]\n}'},
        'industry_data': {'pos': (3, 5.5), 'size': (1.5, 0.8), 'label': '🏢 Industry Data\n{\n  "salary": {...},\n  "demand": "high"\n}'},
        'learning_path': {'pos': (5, 5.5), 'size': (1.5, 0.8), 'label': '🛤️ Learning Path\n{\n  "phases": [...],\n  "timeline": "6mo"\n}'},
        'resources': {'pos': (7, 5.5), 'size': (1.5, 0.8), 'label': '📚 Resources\n{\n  "courses": [...],\n  "search_enabled": true\n}'},
        'web_results': {'pos': (8.5, 4), 'size': (1.2, 0.6), 'label': '🔍 Web Results\n(Tavily API)'},
        'shared_state': {'pos': (4, 3.5), 'size': (2, 0.8), 'label': '💾 CareerPlanningState\n(LangGraph)'},
        'json_response': {'pos': (2, 2), 'size': (2, 0.8), 'label': '📤 JSON Response\n{\n  "learning_path": {...},\n  "resources": {...}\n}'},
        'react_components': {'pos': (6, 2), 'size': (2, 0.8), 'label': '⚛️ React Components\nChat + Flow + Links'}
    }
    
    # Draw data boxes
    for box_id, config in data_boxes.items():
        x, y = config['pos']
        w, h = config['size']
        
        box = FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.05",
            facecolor='#E8F4FD',
            edgecolor='#1976D2',
            linewidth=1.5
        )
        ax.add_patch(box)
        
        ax.text(x, y, config['label'], 
               ha='center', va='center', 
               fontsize=8, fontweight='bold')
    
    # Data flow arrows
    data_flows = [
        ('user_query', 'skills_data'),
        ('user_query', 'industry_data'),
        ('user_query', 'learning_path'),
        ('user_query', 'resources'),
        ('resources', 'web_results'),
        ('skills_data', 'shared_state'),
        ('industry_data', 'shared_state'),
        ('learning_path', 'shared_state'),
        ('resources', 'shared_state'),
        ('shared_state', 'json_response'),
        ('shared_state', 'react_components')
    ]
    
    # Draw data flow arrows
    for start, end in data_flows:
        start_pos = data_boxes[start]['pos']
        end_pos = data_boxes[end]['pos']
        
        arrow = ConnectionPatch(
            start_pos, end_pos, "data", "data",
            arrowstyle="->", shrinkA=20, shrinkB=20,
            mutation_scale=12, fc="blue", alpha=0.6
        )
        ax.add_patch(arrow)
    
    ax.text(5, 7.5, 'CareerPath.AI - Data Flow Architecture', 
           ha='center', va='center', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    return fig

def save_diagrams():
    """Generate and save both diagrams"""
    
    print("🎨 Generating CareerPath.AI Architecture Diagrams...")
    
    # Create agentic architecture diagram
    fig1 = create_agentic_diagram()
    fig1.savefig('careerpath_ai_architecture.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: careerpath_ai_architecture.png")
    
    # Create data flow diagram
    fig2 = create_data_flow_diagram()
    fig2.savefig('careerpath_ai_dataflow.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: careerpath_ai_dataflow.png")
    
    # Display the diagrams
    plt.show()
    
    print("\n📊 Architecture diagrams generated successfully!")
    print("🔍 Files saved:")
    print("   - careerpath_ai_architecture.png (Multi-agent workflow)")
    print("   - careerpath_ai_dataflow.png (Data flow and structures)")

if __name__ == "__main__":
    # Check if required libraries are available
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        save_diagrams()
    except ImportError as e:
        print("❌ Missing required library. Please install:")
        print("pip install matplotlib")
        print(f"Error: {e}") 