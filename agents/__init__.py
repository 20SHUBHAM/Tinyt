"""
AI Agents for Focus Group Platform

This module contains specialized AI agents for different aspects of focus group research:
- PersonaGeneratorAgent: Creates dynamic personas from descriptions
- ContextSchemaGenerator: Generates structured discussion frameworks  
- DynamicFocusGroupAgent: Orchestrates realistic discussions using TinyTroupe
- SummaryAgent: Creates custom reports and summaries
- QAAssistantAgent: Provides interactive Q&A about discussions
"""

from .persona_generator import PersonaGeneratorAgent
from .context_schema_generator import ContextSchemaGenerator
from .focus_group_agent import DynamicFocusGroupAgent
from .summary_agent import SummaryAgent
from .qa_assistant import QAAssistantAgent

__all__ = [
    'PersonaGeneratorAgent',
    'ContextSchemaGenerator', 
    'DynamicFocusGroupAgent',
    'SummaryAgent',
    'QAAssistantAgent'
]