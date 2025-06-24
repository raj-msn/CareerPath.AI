# 🎯 CareerPath.AI Demo Queries

Try these sample queries to see the multi-agent system in action:

## 🚀 NEW: Web Search Feature
The Resources Agent now has **real-time web search** capabilities powered by Tavily! Get current courses, certifications, and learning resources with clickable links.

## 🚀 Basic Career Transitions

### Software Engineer to Senior Engineer
**Query**: "I'm a software engineer with 3 years of experience. I want to become a senior software engineer. What skills do I need to develop?"

**Expected Output**:
- Skills gap analysis (leadership, architecture, system design)
- Industry insights (salary range, market demand)
- Learning roadmap with 3 phases over 6-8 months
- Mermaid diagram showing career progression
- Specific resource recommendations (courses, certifications)

### Product Manager Transition  
**Query**: "I'm a software engineer who wants to transition to product management. Can you help me create a learning path?"

**Expected Output**:
- Technical skills assessment (Python, ML, statistics)
- Industry research on data science market
- Step-by-step learning path with timelines
- Visual roadmap with skill progression
- Resources for Python, machine learning, and data analysis

### Data Science Career
**Query**: "I have a background in mathematics and want to transition into data science. What's the best path forward?"

**Expected Output**:
- Technical skills assessment (Python, ML, statistics)
- Industry research on data science market
- Step-by-step learning path with timelines
- Visual roadmap with skill progression
- Resources for Python, machine learning, and data analysis

## 🎨 Role-Specific Queries

### Marketing Manager Growth
**Query**: "I'm a marketing coordinator. How can I become a marketing manager?"

### Tech Lead Path
**Query**: "I'm a senior developer. What's the path to becoming a tech lead?"

## 🌟 Complex Scenarios

### Career Pivot
**Query**: "I've been a teacher for 5 years and want to transition to UX design"

### Industry Change
**Query**: "I work in finance but want to move to tech. What are my options?"

### Skill-Specific Planning
**Query**: "I need to learn cloud computing for my next role. Create a learning plan."

## 📊 Expected Multi-Agent Behavior

For each query, you should see:

1. **Supervisor Agent** - Analyzes the query and coordinates other agents
2. **Skills Assessment Agent** - Identifies current vs required skills
3. **Industry Research Agent** - Provides market insights and trends
4. **Learning Path Agent** - Creates structured roadmap with Mermaid diagram
5. **Resource Recommendation Agent** - Suggests specific learning materials

## 🎯 Visual Outputs

Each query should generate:
- Comprehensive text response with emojis and formatting
- Mermaid flowchart showing career progression
- Skills gap analysis
- Timeline and milestones
- Specific resource recommendations with links

## 🔧 Testing Tips

1. Start with simple queries first
2. Check that all agents are responding in sequence
3. Verify Mermaid diagrams render properly
4. Test the chat interface responsiveness
5. Try both short and detailed queries

## Follow-up Questions
After getting your initial plan, try these follow-ups:

**Query**: "Can you recommend more beginner-friendly courses?"

**Query**: "What about remote learning options?"

**Query**: "Are there any free alternatives to these resources?"

**Query**: "How can I practice these skills while working full-time?"

## 🔍 Web Search Examples
The system will automatically search for current resources, but you can also ask specifically:

**Query**: "Find me the latest Python courses for 2024"

**Query**: "What are the most recent AWS certifications available?"

**Query**: "Search for active tech communities I can join"

## Advanced Scenarios

### Leadership Transition
**Query**: "I'm a senior developer who wants to move into engineering management. I have strong technical skills but limited people management experience."

### Industry Switch
**Query**: "I'm a finance professional with 5 years experience who wants to transition into tech. I'm interested in fintech specifically."

### Skill Updates
**Query**: "I'm a web developer who learned React 2 years ago. I want to update my skills with the latest technologies and best practices."

## Tips for Best Results

1. **Be specific** about your current experience level
2. **Mention your timeline** (e.g., "within 6 months")
3. **Include constraints** (budget, time availability, location preferences)
4. **Ask follow-up questions** to refine your plan
5. **Check the visual roadmap** on the right panel for timeline details

## ✨ Features Demonstrated

- **Multi-agent coordination** (Supervisor, Skills, Industry, Learning, Resources agents)
- **Real-time web search** for current learning resources
- **Clickable links** to courses, certifications, and platforms
- **Interactive career roadmap** visualization
- **Conversation memory** for follow-up questions
- **Personalized recommendations** based on your background

---

**Note**: The POC uses GPT-4o-mini-2024-07-18, so responses may vary. The multi-agent system ensures comprehensive coverage of all career planning aspects. 

**Note:** Make sure to set your `OPENAI_API_KEY` and `TAVILY_API_KEY` environment variables before running the system. 