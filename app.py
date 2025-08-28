"""
Agentic AI Focus Group Discussion Platform
Flask application with dynamic persona generation and TinyTroupe integration
"""

from flask import Flask, render_template, request, jsonify, session
import os
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv
import logging
from agents.persona_generator import PersonaGeneratorAgent
from agents.context_schema_generator import ContextSchemaGenerator
from agents.focus_group_agent import DynamicFocusGroupAgent
from agents.summary_agent import SummaryAgent
from agents.qa_assistant import QAAssistantAgent
from utils.config import Config
from utils.session_manager import SessionManager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Initialize configuration and session manager
config = Config()
session_manager = SessionManager()

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/api/generate-personas', methods=['POST'])
def generate_personas():
    """Generate personas from free-text description"""
    try:
        logger.info("/api/generate-personas called")
        data = request.get_json()
        description = data.get('description', '')
        num_personas = data.get('num_personas', 6)
        quick_mode = data.get('quick_mode', False)
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        session['current_session'] = session_id
        
        # Initialize persona generator agent
        persona_agent = PersonaGeneratorAgent(config)
        logger.info("PersonaGeneratorAgent initialized")
        
        # Choose generation method based on quick_mode
        if quick_mode:
            personas = persona_agent.generate_quick_personas(description, num_personas)
        else:
            personas = persona_agent.generate_personas(description, num_personas)
        logger.info("Personas generated | count=%s", len(personas) if isinstance(personas, list) else 0)

        if not personas or not isinstance(personas, list):
            logger.error("Persona generation returned no personas; using fallback")
            personas = persona_agent._generate_fallback_personas(description, num_personas)
        logger.info("/api/generate-personas success | personas=%d", len(personas))
        
        # Store personas in session
        logger.info("Storing personas to session: %s", session_id)
        session_manager.store_personas(session_id, personas)
        logger.info("Personas stored for session: %s", session_id)
        
        response_payload = {
            'success': True,
            'session_id': session_id,
            'personas': personas,
            'quick_mode': quick_mode
        }
        logger.info("Returning personas response | size_bytes≈%s", len(json.dumps(response_payload)))
        return jsonify(response_payload), 200
        
    except Exception as e:
        logger.exception(f"Error generating personas: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/update-persona', methods=['POST'])
def update_persona():
    """Update a specific persona"""
    try:
        data = request.get_json()
        session_id = session.get('current_session')
        persona_id = data.get('persona_id')
        updated_persona = data.get('persona')
        
        if not session_id:
            return jsonify({'success': False, 'error': 'No active session'}), 400
            
        session_manager.update_persona(session_id, persona_id, updated_persona)
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Error updating persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-framework', methods=['POST'])
def generate_framework():
    """Generate discussion framework"""
    try:
        data = request.get_json()
        session_id = session.get('current_session')
        topic = data.get('topic', '')
        business_context = data.get('business_context', '')
        duration = data.get('duration', 60)
        
        if not session_id:
            return jsonify({'success': False, 'error': 'No active session'}), 400
            
        # Get personas from session
        personas = session_manager.get_personas(session_id)
        
        # Generate framework
        context_agent = ContextSchemaGenerator(config)
        framework = context_agent.generate_framework(topic, business_context, personas, duration)
        
        # Store framework in session
        session_manager.store_framework(session_id, framework)
        
        return jsonify({
            'success': True,
            'framework': framework
        })
        
    except Exception as e:
        logger.error(f"Error generating framework: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/update-framework', methods=['POST'])
def update_framework():
    """Update discussion framework"""
    try:
        data = request.get_json()
        session_id = session.get('current_session')
        updated_framework = data.get('framework')
        
        if not session_id:
            return jsonify({'success': False, 'error': 'No active session'}), 400
            
        session_manager.store_framework(session_id, updated_framework)
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Error updating framework: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/run-simulation', methods=['POST'])
def run_simulation():
    """Run focus group simulation"""
    try:
        session_id = session.get('current_session')
        
        if not session_id:
            return jsonify({'success': False, 'error': 'No active session'}), 400
            
        # Get personas and framework from session
        personas = session_manager.get_personas(session_id)
        framework = session_manager.get_framework(session_id)
        
        if not personas or not framework:
            return jsonify({'success': False, 'error': 'Missing personas or framework'}), 400
            
        # Run simulation
        focus_group_agent = DynamicFocusGroupAgent(config)
        simulation_result = focus_group_agent.run_simulation(personas, framework, session_id)
        
        # Store results in session
        session_manager.store_simulation(session_id, simulation_result)
        
        return jsonify({
            'success': True,
            'simulation': simulation_result
        })
        
    except Exception as e:
        logger.error(f"Error running simulation: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-summary', methods=['POST'])
def generate_summary():
    """Generate custom summary"""
    try:
        data = request.get_json()
        session_id = session.get('current_session')
        summary_schema = data.get('summary_schema', {})
        
        if not session_id:
            return jsonify({'success': False, 'error': 'No active session'}), 400
            
        # Get simulation results
        simulation = session_manager.get_simulation(session_id)
        
        if not simulation:
            return jsonify({'success': False, 'error': 'No simulation results found'}), 400
            
        # Generate summary
        summary_agent = SummaryAgent(config)
        summary = summary_agent.generate_summary(simulation, summary_schema)
        
        # Store summary
        session_manager.store_summary(session_id, summary)
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ask-question', methods=['POST'])
def ask_question():
    """Ask question about the discussion"""
    try:
        data = request.get_json()
        session_id = session.get('current_session')
        question = data.get('question', '')
        
        if not session_id:
            return jsonify({'success': False, 'error': 'No active session'}), 400
            
        # Get simulation results
        simulation = session_manager.get_simulation(session_id)
        
        if not simulation:
            return jsonify({'success': False, 'error': 'No simulation results found'}), 400
            
        # Get answer
        qa_agent = QAAssistantAgent(config)
        answer = qa_agent.answer_question(simulation, question)
        
        return jsonify({
            'success': True,
            'answer': answer
        })
        
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/suggest-questions', methods=['GET'])
def suggest_questions():
    """Get suggested questions for the discussion"""
    try:
        session_id = session.get('current_session')
        
        if not session_id:
            return jsonify({'success': False, 'error': 'No active session'}), 400
            
        # Get simulation results
        simulation = session_manager.get_simulation(session_id)
        
        if not simulation:
            return jsonify({'success': False, 'error': 'No simulation results found'}), 400
            
        # Get suggested questions
        qa_agent = QAAssistantAgent(config)
        suggestions = qa_agent.suggest_questions(simulation)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export-session', methods=['GET'])
def export_session():
    """Export complete session data"""
    try:
        session_id = session.get('current_session')
        
        if not session_id:
            return jsonify({'success': False, 'error': 'No active session'}), 400
            
        # Get all session data
        export_data = session_manager.export_session(session_id)
        
        return jsonify({
            'success': True,
            'data': export_data
        })
        
    except Exception as e:
        logger.error(f"Error exporting session: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)