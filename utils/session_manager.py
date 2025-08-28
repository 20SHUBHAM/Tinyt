"""
Session management for focus group discussions
"""

import json
import os
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import threading

class SessionManager:
    """Manages session data for focus group discussions"""
    
    def __init__(self, data_dir: str = './data'):
        self.data_dir = data_dir
        self.sessions_file = os.path.join(data_dir, 'sessions.json')
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing sessions
        self._load_sessions()
        
        # Start cleanup thread
        self._start_cleanup_thread()
    
    def _load_sessions(self):
        """Load sessions from disk"""
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r') as f:
                    self.sessions = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.sessions = {}
    
    def _save_sessions(self):
        """Save sessions to disk"""
        with self.lock:
            try:
                with open(self.sessions_file, 'w') as f:
                    json.dump(self.sessions, f, indent=2, default=str)
            except Exception as e:
                print(f"Error saving sessions: {e}")
    
    def _start_cleanup_thread(self):
        """Start background thread to clean up expired sessions"""
        def cleanup():
            while True:
                time.sleep(300)  # Check every 5 minutes
                self._cleanup_expired_sessions()
        
        thread = threading.Thread(target=cleanup, daemon=True)
        thread.start()
    
    def _cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.now()
        expired_sessions = []
        
        with self.lock:
            for session_id, session_data in self.sessions.items():
                last_accessed = datetime.fromisoformat(session_data.get('last_accessed', current_time.isoformat()))
                if current_time - last_accessed > timedelta(hours=1):
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del self.sessions[session_id]
        
        if expired_sessions:
            self._save_sessions()
    
    def _update_last_accessed(self, session_id: str):
        """Update last accessed time for session"""
        if session_id in self.sessions:
            self.sessions[session_id]['last_accessed'] = datetime.now().isoformat()
    
    def create_session(self, session_id: str) -> Dict[str, Any]:
        """Create a new session"""
        session_data = {
            'session_id': session_id,
            'created_at': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat(),
            'personas': [],
            'framework': None,
            'simulation': None,
            'summaries': [],
            'qa_history': []
        }
        
        with self.lock:
            self.sessions[session_id] = session_data
        
        self._save_sessions()
        return session_data
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        with self.lock:
            if session_id in self.sessions:
                self._update_last_accessed(session_id)
                return self.sessions[session_id].copy()
        return None
    
    def store_personas(self, session_id: str, personas: List[Dict[str, Any]]):
        """Store personas for a session"""
        with self.lock:
            if session_id not in self.sessions:
                self.create_session(session_id)
            
            self.sessions[session_id]['personas'] = personas
            self._update_last_accessed(session_id)
        
        self._save_sessions()
    
    def get_personas(self, session_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get personas for a session"""
        session = self.get_session(session_id)
        return session['personas'] if session else None
    
    def update_persona(self, session_id: str, persona_id: str, updated_persona: Dict[str, Any]):
        """Update a specific persona"""
        with self.lock:
            if session_id in self.sessions:
                personas = self.sessions[session_id]['personas']
                for i, persona in enumerate(personas):
                    if persona.get('id') == persona_id:
                        personas[i] = updated_persona
                        break
                self._update_last_accessed(session_id)
        
        self._save_sessions()
    
    def store_framework(self, session_id: str, framework: Dict[str, Any]):
        """Store discussion framework for a session"""
        with self.lock:
            if session_id not in self.sessions:
                self.create_session(session_id)
            
            self.sessions[session_id]['framework'] = framework
            self._update_last_accessed(session_id)
        
        self._save_sessions()
    
    def get_framework(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get framework for a session"""
        session = self.get_session(session_id)
        return session['framework'] if session else None
    
    def store_simulation(self, session_id: str, simulation: Dict[str, Any]):
        """Store simulation results for a session"""
        with self.lock:
            if session_id not in self.sessions:
                self.create_session(session_id)
            
            self.sessions[session_id]['simulation'] = simulation
            self._update_last_accessed(session_id)
        
        self._save_sessions()
    
    def get_simulation(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get simulation results for a session"""
        session = self.get_session(session_id)
        return session['simulation'] if session else None
    
    def store_summary(self, session_id: str, summary: Dict[str, Any]):
        """Store summary for a session"""
        with self.lock:
            if session_id not in self.sessions:
                self.create_session(session_id)
            
            summary['created_at'] = datetime.now().isoformat()
            self.sessions[session_id]['summaries'].append(summary)
            self._update_last_accessed(session_id)
        
        self._save_sessions()
    
    def add_qa_interaction(self, session_id: str, question: str, answer: Dict[str, Any]):
        """Add Q&A interaction to session"""
        with self.lock:
            if session_id not in self.sessions:
                self.create_session(session_id)
            
            interaction = {
                'question': question,
                'answer': answer,
                'timestamp': datetime.now().isoformat()
            }
            self.sessions[session_id]['qa_history'].append(interaction)
            self._update_last_accessed(session_id)
        
        self._save_sessions()
    
    def export_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Export complete session data"""
        session = self.get_session(session_id)
        if session:
            return {
                'export_timestamp': datetime.now().isoformat(),
                'session_data': session
            }
        return None
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all active sessions"""
        with self.lock:
            return [
                {
                    'session_id': session_id,
                    'created_at': data.get('created_at'),
                    'last_accessed': data.get('last_accessed'),
                    'has_personas': bool(data.get('personas')),
                    'has_framework': bool(data.get('framework')),
                    'has_simulation': bool(data.get('simulation')),
                    'summary_count': len(data.get('summaries', [])),
                    'qa_count': len(data.get('qa_history', []))
                }
                for session_id, data in self.sessions.items()
            ]