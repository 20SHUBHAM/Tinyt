"""
LLM client for handling different AI providers
"""

import logging
import json
from typing import Dict, Any, Optional
from openai import OpenAI
import anthropic
import boto3

class LLMClient:
    """Client for interacting with various LLM providers"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.llm_config = config.get_llm_config()
        
        # Initialize appropriate client
        if self.llm_config['provider'] == 'openai':
            # Use new OpenAI client from openai>=1.0
            self.client = OpenAI(api_key=self.llm_config['api_key'])
        elif self.llm_config['provider'] == 'anthropic':
            self.client = anthropic.Anthropic(api_key=self.llm_config['api_key'])
        elif self.llm_config['provider'] == 'bedrock':
            self.client = boto3.client(
                'bedrock-runtime',
                aws_access_key_id=self.llm_config['aws_access_key_id'],
                aws_secret_access_key=self.llm_config['aws_secret_access_key'],
                region_name=self.llm_config['aws_region']
            )
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
            elif self.llm_config['provider'] == 'bedrock':
                return self._generate_bedrock(prompt, max_tokens, temperature)
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
    
    def _generate_bedrock(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate response using AWS Bedrock with Anthropic Claude"""
        
        model_id = self.llm_config['model']
        
        # Prepare the request body for Anthropic Claude models
        if 'claude-3' in model_id:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        else:
            # For older Claude models (claude-v2, claude-instant)
            body = {
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": max_tokens,
                "temperature": temperature,
                "stop_sequences": ["\n\nHuman:"]
            }
        
        try:
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extract text based on model type
            if 'claude-3' in model_id:
                return response_body['content'][0]['text']
            else:
                return response_body['completion']
                
        except Exception as e:
            self.logger.error(f"Bedrock API error: {e}")
            raise
    
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
            
            elif self.llm_config['provider'] == 'bedrock':
                # For Bedrock, combine system and user prompts
                combined_prompt = f"{system_prompt}\n\n{user_prompt}"
                return self._generate_bedrock(combined_prompt, max_tokens, temperature)
                
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