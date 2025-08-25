"""
Base agent class with LLM integration
"""

import logging
from typing import Dict, Any
from utils.llm_client import LLMClient

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_client = LLMClient(config)
        self.agent_name = "BaseAgent"
    
    def _format_prompt(self, template: str, **kwargs) -> str:
        """Format prompt template with variables"""
        try:
            return template.format(**kwargs)
        except KeyError as e:
            self.logger.error(f"Missing template variable: {e}")
            return template
    
    def _extract_json_from_response(self, response: str, start_char: str = '{', end_char: str = '}') -> str:
        """Extract JSON from LLM response"""
        start_idx = response.find(start_char)
        if start_char == '[':
            end_idx = response.rfind(']') + 1
        else:
            end_idx = response.rfind(end_char) + 1
        
        if start_idx == -1 or end_idx <= start_idx:
            raise ValueError(f"No valid JSON found in response")
        
        return response[start_idx:end_idx]
    
    def log_interaction(self, prompt: str, response: str, metadata: Dict[str, Any] = None):
        """Log agent interaction for debugging"""
        if self.config.is_development():
            self.logger.debug(f"Agent: {self.agent_name}")
            self.logger.debug(f"Prompt length: {len(prompt)} chars")
            self.logger.debug(f"Response length: {len(response)} chars")
            if metadata:
                self.logger.debug(f"Metadata: {metadata}")