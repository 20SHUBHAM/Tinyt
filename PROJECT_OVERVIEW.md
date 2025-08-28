# Agentic Focus Group Platform - Project Overview

## 🎯 Project Summary

A complete, production-ready AI-powered platform that conducts realistic focus group discussions using specialized agents and TinyTroupe integration. The platform generates dynamic personas, runs authentic simulations, and extracts actionable business insights through a 5-step automated workflow.

## 🏗️ Architecture Overview

### Core Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │  Flask Backend  │    │  AI Agents      │
│                 │    │                 │    │                 │
│ • HTML/CSS/JS   │◄──►│ • REST API      │◄──►│ • PersonaGen    │
│ • Bootstrap UI  │    │ • Session Mgmt  │    │ • FrameworkGen  │
│ • Real-time UX  │    │ • Error Handle  │    │ • FocusGroupSim │
│                 │    │                 │    │ • SummaryGen    │
│                 │    │                 │    │ • QA Assistant  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Interface│    │  Data Layer     │    │  TinyTroupe     │
│                 │    │                 │    │                 │
│ • Step-by-step  │    │ • Session Store │    │ • AI Personas   │
│ • Progress Track│    │ • File Storage  │    │ • Conversations │
│ • Interactive   │    │ • Export/Import │    │ • Group Dynamic │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Agent System

Each agent is specialized and autonomous:

1. **PersonaGeneratorAgent**: Creates realistic personas from free-text descriptions
2. **ContextSchemaGenerator**: Builds business-focused discussion frameworks  
3. **DynamicFocusGroupAgent**: Orchestrates TinyTroupe simulations
4. **SummaryAgent**: Generates custom reports in multiple formats
5. **QAAssistantAgent**: Provides evidence-based Q&A functionality

## 🔄 5-Step Workflow

### Step 1: Dynamic Persona Creation
- **Input**: Free-text audience description
- **Agent**: PersonaGeneratorAgent
- **Output**: 4-8 detailed personas with authentic backgrounds
- **Features**: Editable personas, diverse demographics, realistic constraints

### Step 2: Framework Generation  
- **Input**: Topic, business context, objectives
- **Agent**: ContextSchemaGenerator
- **Output**: Structured discussion phases with business-focused questions
- **Features**: Customizable framework, timing allocation, moderator guidelines

### Step 3: Focus Group Simulation
- **Input**: Personas + Framework
- **Agent**: DynamicFocusGroupAgent (powered by TinyTroupe)
- **Output**: Complete discussion transcript with natural interactions
- **Features**: Spontaneous reactions, interruptions, group dynamics

### Step 4: Custom Summary Generation
- **Input**: User-defined summary schema
- **Agent**: SummaryAgent
- **Output**: Tailored reports (Executive, Detailed, Insights, Custom)
- **Features**: Multiple formats, business-focused insights, downloadable

### Step 5: Interactive Q&A
- **Input**: User questions about discussion
- **Agent**: QAAssistantAgent  
- **Output**: Evidence-based answers with supporting quotes
- **Features**: Suggested questions, pattern analysis, participant comparisons

## 🛠️ Technical Implementation

### Backend (Flask)
```python
# Core application structure
app.py                 # Main Flask application with REST API
├── /api/generate-personas     # POST - Generate participant personas
├── /api/generate-framework    # POST - Create discussion framework
├── /api/run-simulation       # POST - Execute focus group
├── /api/generate-summary     # POST - Create custom reports
├── /api/ask-question        # POST - Interactive Q&A
├── /api/export-session      # GET  - Export complete data
└── /api/suggest-questions   # GET  - Question suggestions
```

### AI Agents
```python
# Agent hierarchy
agents/
├── base_agent.py           # Base class with LLM integration
├── persona_generator.py    # Dynamic persona creation
├── context_schema_generator.py  # Framework generation
├── focus_group_agent.py    # TinyTroupe orchestration
├── summary_agent.py        # Custom report generation
└── qa_assistant.py         # Interactive Q&A system
```

### Utilities
```python
utils/
├── config.py              # Environment configuration
├── session_manager.py     # Data persistence
└── llm_client.py          # Multi-provider LLM interface
```

### Frontend (HTML/CSS/JS)
```javascript
static/
├── js/
│   ├── app.js            # Core application logic
│   └── focus-group.js    # Workflow-specific functionality
├── css/
│   └── style.css         # Modern responsive UI
└── templates/
    ├── base.html         # Common layout
    ├── index.html        # Main application
    ├── 404.html          # Error pages
    └── 500.html
```

## 🚀 Deployment Options

### Replit (Recommended)
```bash
# Quick deployment
./deploy_replit.sh
# Edit .env with API keys
# Click "Run" button
```

### Docker
```bash
# Build and run
docker-compose up -d
```

### Heroku
```bash
# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

### Manual
```bash
# Local development
python run.py
# Access at http://localhost:5000
```

## 🧪 Key Features

### 1. Dynamic & Configurable
- No hardcoded scenarios or personas
- Fully configurable for any topic/context
- Adaptive discussion frameworks
- Custom summary formats

### 2. Production Ready
- Comprehensive error handling
- Session management and persistence
- Scalable architecture
- Security considerations
- Performance optimization

### 3. Realistic Simulations
- TinyTroupe integration for authentic conversations
- Natural interruptions and reactions
- Group dynamics modeling
- Spontaneous interaction patterns

### 4. Business Intelligence Focus
- Actionable insights extraction
- Strategic recommendations
- Evidence-based analysis
- Multiple report formats

### 5. User Experience
- Step-by-step guided workflow
- Real-time progress tracking
- Interactive editing capabilities
- Modern responsive interface

## 📊 Data Flow

```
User Input → Agent Processing → TinyTroupe Simulation → Analysis → Reports
     ↓              ↓                    ↓              ↓         ↓
Personas     Framework Gen     Conversation      Insights   Summaries
     ↓              ↓                    ↓              ↓         ↓
Session      Discussion        Transcript       Analysis   Export
Storage      Structure         Storage         Engine     Formats
```

## 🔧 Configuration

### Environment Variables
```env
# Required
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key  # OR
ANTHROPIC_API_KEY=your-anthropic-key

# Optional
DEFAULT_LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4
SESSION_TIMEOUT=3600
MAX_SESSIONS=100
```

### Supported LLM Providers
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude-3-sonnet, Claude-3-haiku
- Extensible for additional providers

## 📈 Performance Characteristics

### Scalability
- Session-based architecture
- Stateless API design
- Configurable resource limits
- Background processing support

### Reliability
- Comprehensive error handling
- Graceful degradation
- Fallback mechanisms
- Session recovery

### Security
- Environment-based configuration
- Session isolation
- Input validation
- Safe file operations

## 🎯 Use Cases

### Market Research
- Consumer behavior analysis
- Product feedback collection
- Brand perception studies
- Competitive analysis

### Product Development
- Feature prioritization
- User experience research
- Concept validation
- Usability insights

### Business Strategy
- Market segmentation
- Customer journey mapping
- Pain point identification
- Opportunity analysis

## 🔮 Future Enhancements

### Planned Features
- Multi-language support
- Advanced persona templates
- Real-time collaboration
- Integration APIs
- Advanced analytics

### Technical Improvements
- Redis caching
- Database integration
- Async processing
- Load balancing
- Monitoring/metrics

## 📝 Development Notes

### Code Quality
- Modular agent architecture
- Clean separation of concerns
- Comprehensive error handling
- Type hints and documentation
- Consistent coding standards

### Testing Strategy
- Setup validation script
- Component unit tests
- Integration test scenarios
- End-to-end workflow testing
- Performance benchmarking

### Documentation
- Comprehensive README
- API documentation
- Deployment guides
- Troubleshooting guides
- Architecture overview

## 🎉 Success Metrics

The platform successfully delivers:

1. **Fully Automated Workflow**: No manual intervention required
2. **Production Quality**: Error handling, security, performance
3. **Business Value**: Actionable insights and strategic recommendations
4. **User Experience**: Intuitive interface with guided workflow
5. **Deployment Ready**: Multiple deployment options with documentation
6. **Extensible Architecture**: Easy to add new features and capabilities

---

**This is a complete, production-ready platform that transforms traditional focus group research through AI automation while maintaining the authenticity and insights of human-led discussions.**