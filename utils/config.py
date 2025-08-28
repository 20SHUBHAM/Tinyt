"""
Configuration management for the focus group application
"""

import os
from typing import Dict, Any, List
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
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')  # Modern default model
        self.anthropic_model = os.getenv('ANTHROPIC_MODEL', 'claude-3-haiku-20240307')  # Default to faster model
        
        # AWS Bedrock Configuration
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.bedrock_model = os.getenv('BEDROCK_MODEL', 'anthropic.claude-3-haiku-20240307-v1:0')
        
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
        elif self.default_llm_provider == 'bedrock':
            if not self.aws_access_key_id or not self.aws_secret_access_key:
                raise ValueError("AWS credentials not configured for Bedrock")
            return {
                'provider': 'bedrock',
                'aws_access_key_id': self.aws_access_key_id,
                'aws_secret_access_key': self.aws_secret_access_key,
                'aws_region': self.aws_region,
                'model': self.bedrock_model
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
    
    def get_available_providers(self) -> List[str]:
        """Get list of available LLM providers based on configuration"""
        providers = []
        
        if self.openai_api_key:
            providers.append('openai')
        if self.anthropic_api_key:
            providers.append('anthropic')
        if self.aws_access_key_id and self.aws_secret_access_key:
            providers.append('bedrock')
            
        return providers