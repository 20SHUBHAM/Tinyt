"""
ContextSchemaGenerator - Generates structured discussion frameworks for focus groups
"""

import json
import uuid
from typing import List, Dict, Any
from .base_agent import BaseAgent

class ContextSchemaGenerator(BaseAgent):
    """Agent responsible for generating structured discussion frameworks"""
    
    def __init__(self, config):
        super().__init__(config)
        self.agent_name = "ContextSchemaGenerator"
    
    def generate_framework(self, topic: str, business_context: str, 
                         personas: List[Dict[str, Any]], duration: int = 60) -> Dict[str, Any]:
        """
        Generate a structured discussion framework
        
        Args:
            topic: Main discussion topic
            business_context: Business perspective and goals
            personas: List of participant personas
            duration: Discussion duration in minutes
            
        Returns:
            Structured discussion framework
        """
        
        persona_summary = self._summarize_personas(personas)
        
        prompt = f"""
        You are an expert focus group moderator and business research specialist. Create a comprehensive, 
        structured discussion framework for a focus group session.
        
        **Discussion Topic:** {topic}
        
        **Business Context:** {business_context}
        
        **Target Duration:** {duration} minutes
        
        **Participant Profile Summary:**
        {persona_summary}
        
        Design a framework that maximizes business value while ensuring natural, engaging conversations.
        The framework should be adaptive to group dynamics and include contingency options.
        
        Create a structured framework with the following components:
        
        1. **Session Overview**:
           - Objectives (business and research goals)
           - Key research questions to answer
           - Success metrics for the session
           - Expected deliverables
        
        2. **Discussion Phases** (4-6 phases):
           For each phase, include:
           - Phase name and objective
           - Duration allocation
           - Primary questions (2-3 main questions)
           - Follow-up probes (specific follow-ups based on likely responses)
           - Transition strategy to next phase
           - Business insights to capture
        
        3. **Moderator Guidelines**:
           - Opening strategy
           - Techniques for managing different personality types
           - Methods to encourage participation from quiet members
           - Strategies for handling dominant participants
           - Ways to navigate disagreements productively
        
        4. **Business Intelligence Focus**:
           - Key metrics and KPIs to extract
           - Competitive insights to gather
           - Pain points to identify
           - Opportunity areas to explore
           - Decision-making factors to understand
        
        5. **Dynamic Adaptations**:
           - Contingency questions if discussion stalls
           - Alternative angles if participants aren't engaging
           - Options to extend or shorten phases based on engagement
           - Backup topics for unexpected silence
        
        6. **Closing Strategy**:
           - Summary and validation approach
           - Final insight-gathering questions
           - Next steps communication
        
        IMPORTANT CONSIDERATIONS:
        - Design questions that encourage storytelling and specific examples
        - Include business-focused probes that reveal actionable insights
        - Ensure logical flow between phases
        - Account for natural energy patterns (engagement, fatigue)
        - Include timing flexibility while maintaining structure
        - Consider group dynamics based on persona mix
        
        Return the framework as a structured JSON object:
        
        {{
            "framework_id": "unique_id",
            "topic": "topic",
            "business_context": "context",
            "duration_minutes": number,
            "session_overview": {{
                "objectives": ["objective1", "objective2"],
                "key_research_questions": ["question1", "question2"],
                "success_metrics": ["metric1", "metric2"],
                "expected_deliverables": ["deliverable1", "deliverable2"]
            }},
            "discussion_phases": [
                {{
                    "phase_id": "unique_id",
                    "name": "Phase Name",
                    "objective": "What this phase aims to achieve",
                    "duration_minutes": number,
                    "primary_questions": [
                        {{
                            "question": "Main question text",
                            "rationale": "Why this question is important",
                            "expected_insights": ["insight1", "insight2"]
                        }}
                    ],
                    "follow_up_probes": [
                        {{
                            "probe": "Follow-up question",
                            "trigger": "When to use this probe",
                            "purpose": "What this probe reveals"
                        }}
                    ],
                    "transition_strategy": "How to move to next phase",
                    "business_focus": ["business insight1", "business insight2"]
                }}
            ],
            "moderator_guidelines": {{
                "opening_strategy": "How to start the session",
                "personality_management": {{
                    "quiet_participants": "Strategies for encouraging participation",
                    "dominant_participants": "Strategies for managing over-participation",
                    "skeptical_participants": "Approaches for engaging skeptics",
                    "enthusiastic_participants": "Ways to channel enthusiasm productively"
                }},
                "conflict_resolution": "How to handle disagreements",
                "energy_management": "Maintaining engagement throughout"
            }},
            "business_intelligence_focus": {{
                "key_metrics": ["metric1", "metric2"],
                "competitive_insights": ["area1", "area2"],
                "pain_points_to_identify": ["pain1", "pain2"],
                "opportunity_areas": ["opportunity1", "opportunity2"],
                "decision_factors": ["factor1", "factor2"]
            }},
            "dynamic_adaptations": {{
                "if_discussion_stalls": ["strategy1", "strategy2"],
                "if_low_engagement": ["approach1", "approach2"],
                "time_adjustments": {{
                    "extend_options": ["option1", "option2"],
                    "shorten_options": ["option1", "option2"]
                }},
                "backup_topics": ["topic1", "topic2"]
            }},
            "closing_strategy": {{
                "summary_approach": "How to summarize findings",
                "validation_questions": ["question1", "question2"],
                "final_insights": ["insight area1", "insight area2"],
                "next_steps": "Communication about follow-up"
            }}
        }}
        
        Ensure the framework is professional, business-focused, and designed to generate maximum actionable insights.
        """
        
        try:
            response = self.llm_client.generate(prompt, max_tokens=6000, temperature=0.3)
            
            # Extract JSON from response
            json_str = self._extract_json_from_response(response, '{', '}')
            framework = json.loads(json_str)
            
            # Add ID if not present
            if 'framework_id' not in framework:
                framework['framework_id'] = str(uuid.uuid4())
            
            # Add metadata
            framework['created_at'] = json.dumps({"timestamp": "now"})
            framework['persona_count'] = len(personas)
            
            return framework
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse framework JSON: {e}")
            return self._generate_fallback_framework(topic, business_context, duration)
        
        except Exception as e:
            self.logger.error(f"Error generating framework: {e}")
            return self._generate_fallback_framework(topic, business_context, duration)
    
    def _summarize_personas(self, personas: List[Dict[str, Any]]) -> str:
        """Create a summary of personas for framework generation"""
        
        if not personas:
            return "No specific personas provided"
        
        summary_parts = []
        
        for persona in personas:
            name = persona.get('name', 'Unnamed')
            demographics = persona.get('demographics', {})
            discussion_style = persona.get('discussion_style', {})
            
            age = demographics.get('age', 'Unknown age')
            occupation = demographics.get('occupation', 'Unknown occupation')
            participation = discussion_style.get('participation_level', 'medium')
            tendency = discussion_style.get('agreement_tendency', 'balanced')
            
            summary_parts.append(f"- {name}: {age}, {occupation}, {participation} participation, {tendency} tendency")
        
        return "\n".join(summary_parts)
    
    def _generate_fallback_framework(self, topic: str, business_context: str, duration: int) -> Dict[str, Any]:
        """Generate a basic fallback framework if main generation fails"""
        
        framework_id = str(uuid.uuid4())
        
        return {
            "framework_id": framework_id,
            "topic": topic,
            "business_context": business_context,
            "duration_minutes": duration,
            "session_overview": {
                "objectives": [
                    "Understand participant perspectives on the topic",
                    "Identify key insights for business decisions"
                ],
                "key_research_questions": [
                    "What are the main challenges participants face?",
                    "What solutions would be most valuable?"
                ],
                "success_metrics": [
                    "Clear participant perspectives captured",
                    "Actionable business insights identified"
                ],
                "expected_deliverables": [
                    "Discussion transcript",
                    "Key insights summary"
                ]
            },
            "discussion_phases": [
                {
                    "phase_id": str(uuid.uuid4()),
                    "name": "Opening & Introductions",
                    "objective": "Create comfort and establish context",
                    "duration_minutes": 10,
                    "primary_questions": [
                        {
                            "question": "Tell us about yourself and your experience with this topic",
                            "rationale": "Establish baseline and comfort level",
                            "expected_insights": ["Experience levels", "Initial perspectives"]
                        }
                    ],
                    "follow_up_probes": [
                        {
                            "probe": "What specific challenges have you faced?",
                            "trigger": "When participants mention difficulties",
                            "purpose": "Identify pain points"
                        }
                    ],
                    "transition_strategy": "Build on shared experiences to move to main discussion",
                    "business_focus": ["Target audience validation", "Experience mapping"]
                },
                {
                    "phase_id": str(uuid.uuid4()),
                    "name": "Core Discussion",
                    "objective": "Explore main topic in depth",
                    "duration_minutes": 30,
                    "primary_questions": [
                        {
                            "question": "Walk us through your typical process or experience",
                            "rationale": "Understand current state and workflow",
                            "expected_insights": ["Current processes", "Decision factors"]
                        }
                    ],
                    "follow_up_probes": [
                        {
                            "probe": "What would make this better for you?",
                            "trigger": "When frustrations are mentioned",
                            "purpose": "Identify improvement opportunities"
                        }
                    ],
                    "transition_strategy": "Focus on specific improvement areas",
                    "business_focus": ["Process insights", "Improvement opportunities"]
                },
                {
                    "phase_id": str(uuid.uuid4()),
                    "name": "Solutions & Preferences",
                    "objective": "Explore desired solutions and preferences",
                    "duration_minutes": 15,
                    "primary_questions": [
                        {
                            "question": "What would an ideal solution look like to you?",
                            "rationale": "Understand preferred outcomes",
                            "expected_insights": ["Solution preferences", "Priority features"]
                        }
                    ],
                    "follow_up_probes": [
                        {
                            "probe": "How would you prioritize these features?",
                            "trigger": "When multiple preferences mentioned",
                            "purpose": "Understand priority ranking"
                        }
                    ],
                    "transition_strategy": "Summarize key themes for validation",
                    "business_focus": ["Feature priorities", "Solution validation"]
                },
                {
                    "phase_id": str(uuid.uuid4()),
                    "name": "Wrap-up & Validation",
                    "objective": "Confirm understanding and gather final insights",
                    "duration_minutes": 5,
                    "primary_questions": [
                        {
                            "question": "What's the most important takeaway from our discussion?",
                            "rationale": "Confirm key insights",
                            "expected_insights": ["Priority themes", "Key messages"]
                        }
                    ],
                    "follow_up_probes": [
                        {
                            "probe": "Is there anything important we haven't discussed?",
                            "trigger": "Always ask at the end",
                            "purpose": "Capture missing insights"
                        }
                    ],
                    "transition_strategy": "Close with appreciation and next steps",
                    "business_focus": ["Insight validation", "Missing gaps"]
                }
            ],
            "moderator_guidelines": {
                "opening_strategy": "Create warm, welcoming environment with clear expectations",
                "personality_management": {
                    "quiet_participants": "Use direct but gentle questions to encourage participation",
                    "dominant_participants": "Politely redirect to ensure balanced participation",
                    "skeptical_participants": "Acknowledge concerns and explore underlying reasons",
                    "enthusiastic_participants": "Channel energy positively while managing time"
                },
                "conflict_resolution": "Acknowledge different perspectives and find common ground",
                "energy_management": "Monitor engagement and adjust pacing as needed"
            },
            "business_intelligence_focus": {
                "key_metrics": ["Satisfaction levels", "Usage patterns"],
                "competitive_insights": ["Alternative solutions", "Switching factors"],
                "pain_points_to_identify": ["Process inefficiencies", "Unmet needs"],
                "opportunity_areas": ["Innovation possibilities", "Service gaps"],
                "decision_factors": ["Priority criteria", "Budget considerations"]
            },
            "dynamic_adaptations": {
                "if_discussion_stalls": ["Ask for specific examples", "Introduce hypothetical scenarios"],
                "if_low_engagement": ["Shift to smaller group discussions", "Use more interactive techniques"],
                "time_adjustments": {
                    "extend_options": ["Deep dive on key topics", "Additional follow-up questions"],
                    "shorten_options": ["Focus on priority questions", "Combine similar phases"]
                },
                "backup_topics": ["Related experiences", "Future aspirations"]
            },
            "closing_strategy": {
                "summary_approach": "Highlight key themes and validate understanding",
                "validation_questions": [
                    "Does this summary capture your main points?",
                    "What would you add or change?"
                ],
                "final_insights": ["Priority themes", "Action implications"],
                "next_steps": "Explain how insights will be used and thank participants"
            },
            "created_at": json.dumps({"timestamp": "now"}),
            "persona_count": 0,
            "fallback": True
        }
    
    def customize_framework(self, framework: Dict[str, Any], 
                          customizations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Customize an existing framework based on user input
        
        Args:
            framework: Original framework
            customizations: User customization requests
            
        Returns:
            Updated framework
        """
        
        prompt = f"""
        You are customizing a focus group discussion framework based on user feedback.
        
        Original Framework:
        {json.dumps(framework, indent=2)}
        
        User Customization Requests:
        {json.dumps(customizations, indent=2)}
        
        Please update the framework to incorporate the user's customization requests while maintaining 
        the overall structure and business focus. Ensure all timing allocations still add up appropriately 
        and that the flow remains logical.
        
        Return the updated framework as JSON with the same structure as the original.
        """
        
        try:
            response = self.llm_client.generate(prompt, max_tokens=6000, temperature=0.3)
            
            # Extract JSON from response
            json_str = self._extract_json_from_response(response, '{', '}')
            updated_framework = json.loads(json_str)
            
            # Preserve original ID
            updated_framework['framework_id'] = framework['framework_id']
            
            return updated_framework
            
        except Exception as e:
            self.logger.error(f"Error customizing framework: {e}")
            return framework  # Return original if customization fails