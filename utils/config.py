"""
Configuration management for the focus group application
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    def __init__(self):
        self.flask_env = os.getenv('FLASK_ENV', 'production')
        self.secret_key = os.getenv('SECRET_KEY', 'change-me-in-production')
        self.port = int(os.getenv('PORT', 5000))
        
        # LLM Configuration
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.default_llm_provider = os.getenv('DEFAULT_LLM_PROVIDER', 'openai')
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')  # Default to faster model
        self.anthropic_model = os.getenv('ANTHROPIC_MODEL', 'claude-3-haiku-20240307')  # Default to faster model
        
        # TinyTroupe Configuration
        self.tinytroupe_cache_dir = os.getenv('TINYTROUPE_CACHE_DIR', './cache')
        self.tinytroupe_log_level = os.getenv('TINYTROUPE_LOG_LEVEL', 'INFO')
        
        # Session Configuration
        self.session_timeout = int(os.getenv('SESSION_TIMEOUT', 3600))
        self.max_sessions = int(os.getenv('MAX_SESSIONS', 100))
        
        # Ensure cache directory exists
        os.makedirs(self.tinytroupe_cache_dir, exist_ok=True)
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration based on provider"""
        if self.default_llm_provider == 'openai':
            if not self.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            return {
                'provider': 'openai',
                'api_key': self.openai_api_key,
                'model': self.openai_model
            }
        elif self.default_llm_provider == 'anthropic':
            if not self.anthropic_api_key:
                raise ValueError("Anthropic API key not configured")
            return {
                'provider': 'anthropic',
                'api_key': self.anthropic_api_key,
                'model': self.anthropic_model
            }
        else:
            raise ValueError(f"Unsupported LLM provider: {self.default_llm_provider}")
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.flask_env == 'development'
    
    def validate_config(self) -> bool:
        """Validate essential configuration"""
        try:
            self.get_llm_config()
            return True
        except ValueError:
            return False