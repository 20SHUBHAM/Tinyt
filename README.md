# Agentic Focus Group Platform

An AI-powered platform for conducting realistic focus group discussions using specialized agents and TinyTroupe integration. Generate dynamic personas, run authentic simulations, and extract actionable business insights.

## Features

### 🤖 AI-Powered Agents
- **PersonaGeneratorAgent**: Creates diverse, realistic personas from free-text descriptions
- **ContextSchemaGenerator**: Generates structured discussion frameworks with business focus
- **DynamicFocusGroupAgent**: Orchestrates realistic discussions using TinyTroupe
- **SummaryAgent**: Creates custom reports in multiple formats
- **QAAssistantAgent**: Provides interactive Q&A about discussions

### 🔄 5-Step Workflow
1. **Dynamic Persona Creation**: Generate detailed participant profiles
2. **Framework Generation**: Create structured discussion phases
3. **Focus Group Simulation**: Run realistic conversations with group dynamics
4. **Custom Summary Generation**: Generate reports tailored to your needs
5. **Interactive Q&A**: Ask questions and get evidence-based answers

### 🚀 Production Ready
- Flask web application with modern UI
- Session management and data persistence
- Error handling and fallback mechanisms
- Configurable LLM providers (OpenAI, Anthropic)
- Ready for deployment on Replit, Heroku, and other platforms

## Quick Start

### Prerequisites
- Python 3.11+
- API key for OpenAI or Anthropic

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd agentic-focus-group
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the application**:
```bash
python app.py
```

5. **Open your browser** to `http://localhost:5000`

### Environment Configuration

Create a `.env` file with the following variables:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
PORT=5000

# LLM API Keys (choose one or more)
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Default LLM Provider
DEFAULT_LLM_PROVIDER=openai

# Model Configuration
OPENAI_MODEL=gpt-4
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# TinyTroupe Configuration
TINYTROUPE_CACHE_DIR=./cache
TINYTROUPE_LOG_LEVEL=INFO

# Session Configuration
SESSION_TIMEOUT=3600
MAX_SESSIONS=100
```

## Usage Guide

### Step 1: Generate Personas
- Provide a free-text description of your target audience
- Choose the number of personas (4-8 recommended)
- AI generates diverse, realistic participant profiles
- Review and edit personas as needed

### Step 2: Create Discussion Framework
- Define your discussion topic and business context
- Set session duration and objectives
- AI generates structured phases with business-focused questions
- Customize framework based on your specific needs

### Step 3: Run Simulation
- TinyTroupe agents conduct realistic focus group discussion
- Natural interruptions and group dynamics
- Spontaneous reactions and authentic conversations
- Real-time analysis and insights

### Step 4: Generate Summaries
Choose from multiple summary formats:
- **Executive Summary**: High-level insights for stakeholders
- **Detailed Report**: Comprehensive analysis with methodology
- **Insights Only**: Focused on actionable intelligence
- **Custom Format**: Define your own structure

### Step 5: Interactive Q&A
- Ask specific questions about the discussion
- Get evidence-based answers with supporting quotes
- Suggested questions based on discussion content
- Pattern analysis and participant comparisons

## API Endpoints

### Core Workflow
- `POST /api/generate-personas` - Generate participant personas
- `POST /api/generate-framework` - Create discussion framework
- `POST /api/run-simulation` - Execute focus group simulation
- `POST /api/generate-summary` - Create custom summaries
- `POST /api/ask-question` - Interactive Q&A

### Data Management
- `POST /api/update-persona` - Edit persona details
- `POST /api/update-framework` - Modify discussion framework
- `GET /api/suggest-questions` - Get question suggestions
- `GET /api/export-session` - Export complete session data

## Architecture

### Agent System
Each agent is specialized for specific tasks:

```python
# Example: Using the PersonaGeneratorAgent
from agents.persona_generator import PersonaGeneratorAgent
from utils.config import Config

config = Config()
agent = PersonaGeneratorAgent(config)
personas = agent.generate_personas("College students interested in fitness", 6)
```

### TinyTroupe Integration
- Creates realistic AI participants with detailed backgrounds
- Simulates natural group dynamics and conversations
- Handles spontaneous reactions and interruptions
- Generates authentic discussion transcripts

### Session Management
- Persistent session storage
- Automatic cleanup of expired sessions
- Export functionality for complete workflows
- Thread-safe operations

## Deployment

### Replit Deployment
1. Fork this repository to Replit
2. Set environment variables in Replit Secrets
3. Run the application
4. Share the generated URL

### Heroku Deployment
```bash
# Install Heroku CLI and login
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your-key
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

## Configuration Options

### LLM Providers
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude-3-sonnet, Claude-3-haiku

### TinyTroupe Settings
- Cache directory for session persistence
- Logging levels and output control
- Agent behavior customization

### Performance Tuning
- Session timeout configuration
- Maximum concurrent sessions
- Worker process settings

## Development

### Project Structure
```
├── app.py                 # Main Flask application
├── agents/               # AI agent implementations
│   ├── persona_generator.py
│   ├── context_schema_generator.py
│   ├── focus_group_agent.py
│   ├── summary_agent.py
│   └── qa_assistant.py
├── utils/                # Utility modules
│   ├── config.py
│   ├── session_manager.py
│   └── llm_client.py
├── templates/            # HTML templates
├── static/              # CSS and JavaScript
└── tests/               # Test suite
```

### Adding New Features
1. Create new agent in `agents/` directory
2. Extend base agent class
3. Add API endpoints in `app.py`
4. Update frontend interface
5. Add tests and documentation

### Testing
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black .

# Linting
flake8
```

## Troubleshooting

### Common Issues

**1. API Key Errors**
```
Error: OpenAI API key not configured
```
- Ensure API key is set in environment variables
- Check key validity and permissions

**2. TinyTroupe Import Errors**
```
ImportError: No module named 'tinytroupe'
```
- Install TinyTroupe: `pip install tinytroupe`
- Check Python environment and dependencies

**3. Session Timeout**
```
Error: No active session
```
- Sessions expire after 1 hour by default
- Start a new session or adjust timeout settings

**4. Memory Issues**
```
Out of memory during simulation
```
- Reduce number of personas
- Shorten discussion duration
- Use smaller LLM models

### Performance Optimization
- Use caching for repeated operations
- Implement request queuing for high load
- Monitor session memory usage
- Configure appropriate worker processes

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Ensure code passes linting: `black . && flake8`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the documentation
- Review example configurations

## Roadmap

### Upcoming Features
- [ ] Multi-language support
- [ ] Advanced persona templates
- [ ] Integration with survey platforms
- [ ] Real-time collaboration features
- [ ] Advanced analytics dashboard
- [ ] API rate limiting and authentication
- [ ] Webhook integrations
- [ ] Custom agent training

### Performance Improvements
- [ ] Async processing for simulations
- [ ] Redis caching layer
- [ ] Database integration
- [ ] Load balancing support
- [ ] Monitoring and metrics

---

**Built with ❤️ for researchers, product managers, and business analysts who need authentic consumer insights.**