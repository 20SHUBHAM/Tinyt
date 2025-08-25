"""
LLM client for handling different AI providers
"""

import logging
from typing import Dict, Any, Optional
import openai
import anthropic

class LLMClient:
    """Client for interacting with various LLM providers"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.llm_config = config.get_llm_config()
        
        # Initialize appropriate client
        if self.llm_config['provider'] == 'openai':
            self.client = openai.OpenAI(api_key=self.llm_config['api_key'])
        elif self.llm_config['provider'] == 'anthropic':
            self.client = anthropic.Anthropic(api_key=self.llm_config['api_key'])
        else:
            raise ValueError(f"Unsupported provider: {self.llm_config['provider']}")
    
    def generate(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> str:
        """
        Generate text using the configured LLM
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text response
        """
        
        try:
            if self.llm_config['provider'] == 'openai':
                return self._generate_openai(prompt, max_tokens, temperature)
            elif self.llm_config['provider'] == 'anthropic':
                return self._generate_anthropic(prompt, max_tokens, temperature)
            else:
                raise ValueError(f"Unsupported provider: {self.llm_config['provider']}")
                
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            raise
    
    def _generate_openai(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate response using OpenAI"""
        
        response = self.client.chat.completions.create(
            model=self.llm_config['model'],
            messages=[
                {"role": "system", "content": "You are an expert AI assistant specialized in market research, consumer psychology, and focus group facilitation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=60  # 60 second timeout
        )
        
        return response.choices[0].message.content
    
    def _generate_anthropic(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate response using Anthropic Claude"""
        
        response = self.client.messages.create(
            model=self.llm_config['model'],
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    def generate_with_system_prompt(self, system_prompt: str, user_prompt: str, 
                                  max_tokens: int = 4000, temperature: float = 0.7) -> str:
        """
        Generate with separate system and user prompts (OpenAI style)
        
        Args:
            system_prompt: System instruction prompt
            user_prompt: User message prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text response
        """
        
        try:
            if self.llm_config['provider'] == 'openai':
                response = self.client.chat.completions.create(
                    model=self.llm_config['model'],
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content
                
            elif self.llm_config['provider'] == 'anthropic':
                # Anthropic handles system prompt differently
                combined_prompt = f"<system>{system_prompt}</system>\n\n{user_prompt}"
                response = self.client.messages.create(
                    model=self.llm_config['model'],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=[
                        {"role": "user", "content": combined_prompt}
                    ]
                )
                return response.content[0].text
                
        except Exception as e:
            self.logger.error(f"Error generating response with system prompt: {e}")
            raise
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text (rough approximation)
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Estimated token count
        """
        # Rough approximation: 1 token ≈ 4 characters
        return len(text) // 4