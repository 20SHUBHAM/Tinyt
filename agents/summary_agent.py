"""
SummaryAgent - Generates custom summaries and reports from focus group discussions
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class SummaryAgent(BaseAgent):
    """Agent responsible for generating customized summaries and reports"""
    
    def __init__(self, config):
        super().__init__(config)
        self.agent_name = "SummaryAgent"
    
    def generate_summary(self, simulation_data: Dict[str, Any], 
                        summary_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a custom summary based on user-defined schema
        
        Args:
            simulation_data: Complete simulation results
            summary_schema: User-defined summary structure and requirements
            
        Returns:
            Generated summary following the specified schema
        """
        
        summary_type = summary_schema.get('type', 'comprehensive')
        
        if summary_type == 'executive':
            return self._generate_executive_summary(simulation_data, summary_schema)
        elif summary_type == 'detailed':
            return self._generate_detailed_report(simulation_data, summary_schema)
        elif summary_type == 'insights_only':
            return self._generate_insights_summary(simulation_data, summary_schema)
        elif summary_type == 'custom':
            return self._generate_custom_summary(simulation_data, summary_schema)
        else:
            return self._generate_comprehensive_summary(simulation_data, summary_schema)
    
    def _generate_executive_summary(self, simulation_data: Dict[str, Any], 
                                  schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive-level summary for business stakeholders"""
        
        conversation_log = simulation_data.get('simulation_results', {}).get('conversation_log', [])
        analysis = simulation_data.get('analysis', {})
        
        # Extract key content for analysis
        key_content = self._extract_key_content(conversation_log)
        
        prompt = f"""
        Create an executive summary for business stakeholders based on this focus group discussion.
        
        Discussion Data:
        Topic: {simulation_data.get('framework_used', 'Market Research')}
        Participants: {simulation_data.get('participants', 0)}
        Duration: {simulation_data.get('metadata', {}).get('duration_minutes', 60)} minutes
        
        Key Discussion Content:
        {json.dumps(key_content, indent=2)}
        
        Analysis Insights:
        {json.dumps(analysis, indent=2)}
        
        Create an executive summary with:
        1. **Executive Overview** (2-3 sentences)
        2. **Key Findings** (3-5 bullet points)
        3. **Business Implications** (3-4 strategic points)
        4. **Recommended Actions** (3-4 specific next steps)
        5. **Investment Priorities** (ranked list)
        6. **Risk Factors** (potential challenges)
        
        Focus on actionable insights that support business decision-making.
        Use clear, business-oriented language suitable for C-level executives.
        
        Return as JSON:
        {{
            "summary_type": "executive",
            "executive_overview": "brief overview",
            "key_findings": ["finding1", "finding2", "finding3"],
            "business_implications": [
                {{
                    "area": "business area",
                    "implication": "what this means",
                    "impact": "high/medium/low"
                }}
            ],
            "recommended_actions": [
                {{
                    "action": "specific action",
                    "priority": "high/medium/low",
                    "timeline": "timeframe",
                    "resources_needed": "resources"
                }}
            ],
            "investment_priorities": [
                {{
                    "priority": "investment area",
                    "rationale": "why this is important",
                    "expected_roi": "potential return"
                }}
            ],
            "risk_factors": ["risk1", "risk2"],
            "confidence_level": "high/medium/low"
        }}
        """
        
        try:
            response = self.llm_client.generate(prompt, max_tokens=3000, temperature=0.2)
            json_str = self._extract_json_from_response(response, '{', '}')
            summary = json.loads(json_str)
            
            # Add metadata
            summary['generated_at'] = datetime.now().isoformat()
            summary['summary_id'] = str(uuid.uuid4())
            summary['source_simulation'] = simulation_data.get('simulation_id')
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating executive summary: {e}")
            return self._generate_fallback_summary(simulation_data, "executive")
    
    def _generate_detailed_report(self, simulation_data: Dict[str, Any], 
                                schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed analytical report"""
        
        conversation_log = simulation_data.get('simulation_results', {}).get('conversation_log', [])
        analysis = simulation_data.get('analysis', {})
        dynamics = simulation_data.get('simulation_results', {}).get('discussion_dynamics', {})
        
        sections_requested = schema.get('sections', [
            'methodology', 'participant_profiles', 'discussion_flow', 
            'key_insights', 'verbatim_quotes', 'recommendations'
        ])
        
        prompt = f"""
        Create a detailed research report based on this focus group discussion.
        
        Simulation Data:
        {json.dumps(simulation_data, indent=2)[:5000]}...
        
        Include these sections: {sections_requested}
        
        Generate a comprehensive report with:
        
        1. **Methodology & Approach**
           - Research design and objectives
           - Participant recruitment criteria
           - Discussion framework and timing
        
        2. **Participant Profiles**
           - Demographic breakdown
           - Psychographic characteristics
           - Relevant experience levels
        
        3. **Discussion Flow Analysis**
           - Phase-by-phase breakdown
           - Engagement patterns
           - Group dynamics observations
        
        4. **Key Insights & Findings**
           - Major themes identified
           - Consensus vs. conflicting views
           - Unexpected discoveries
        
        5. **Supporting Evidence**
           - Relevant verbatim quotes
           - Quantitative observations
           - Behavioral patterns noted
        
        6. **Strategic Recommendations**
           - Short-term tactical moves
           - Long-term strategic considerations
           - Implementation suggestions
        
        7. **Appendices**
           - Complete discussion transcript summary
           - Participant interaction matrix
           - Spontaneous reaction analysis
        
        Return as structured JSON with each section clearly defined.
        """
        
        try:
            response = self.llm_client.generate(prompt, max_tokens=6000, temperature=0.3)
            json_str = self._extract_json_from_response(response, '{', '}')
            report = json.loads(json_str)
            
            # Add metadata
            report['report_type'] = 'detailed'
            report['generated_at'] = datetime.now().isoformat()
            report['summary_id'] = str(uuid.uuid4())
            report['source_simulation'] = simulation_data.get('simulation_id')
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating detailed report: {e}")
            return self._generate_fallback_summary(simulation_data, "detailed")
    
    def _generate_insights_summary(self, simulation_data: Dict[str, Any], 
                                 schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights-focused summary"""
        
        analysis = simulation_data.get('analysis', {})
        conversation_log = simulation_data.get('simulation_results', {}).get('conversation_log', [])
        
        insights_focus = schema.get('focus_areas', [
            'consumer_behavior', 'pain_points', 'opportunities', 'preferences'
        ])
        
        prompt = f"""
        Extract and organize key insights from this focus group discussion.
        
        Focus Areas: {insights_focus}
        
        Analysis Data:
        {json.dumps(analysis, indent=2)}
        
        Raw Discussion Themes:
        {self._extract_themes_from_conversation(conversation_log)}
        
        Create an insights summary with:
        
        1. **Core Consumer Insights**
           - Behavioral patterns discovered
           - Motivational drivers identified
           - Decision-making factors
        
        2. **Pain Point Analysis**
           - Current frustrations and challenges
           - Unmet needs identified
           - Process inefficiencies
        
        3. **Opportunity Mapping**
           - Market gaps identified
           - Innovation opportunities
           - Service enhancement areas
        
        4. **Preference Patterns**
           - Feature preferences ranked
           - Communication preferences
           - Channel preferences
        
        5. **Segment Characteristics**
           - Distinct user groups identified
           - Segment-specific needs
           - Targeting implications
        
        6. **Actionable Intelligence**
           - Immediately implementable insights
           - Testing hypotheses to validate
           - Metrics to track
        
        Focus on insights that are:
        - Specific and actionable
        - Backed by evidence from the discussion
        - Relevant to business strategy
        - Unexpected or counter-intuitive findings
        
        Return as JSON with clear insight categories and supporting evidence.
        """
        
        try:
            response = self.llm_client.generate(prompt, max_tokens=4000, temperature=0.3)
            json_str = self._extract_json_from_response(response, '{', '}')
            insights = json.loads(json_str)
            
            # Add metadata
            insights['summary_type'] = 'insights_only'
            insights['generated_at'] = datetime.now().isoformat()
            insights['summary_id'] = str(uuid.uuid4())
            insights['source_simulation'] = simulation_data.get('simulation_id')
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating insights summary: {e}")
            return self._generate_fallback_summary(simulation_data, "insights")
    
    def _generate_custom_summary(self, simulation_data: Dict[str, Any], 
                               schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary based on custom user schema"""
        
        custom_template = schema.get('template', {})
        custom_sections = schema.get('custom_sections', [])
        output_format = schema.get('output_format', 'structured')
        
        conversation_log = simulation_data.get('simulation_results', {}).get('conversation_log', [])
        analysis = simulation_data.get('analysis', {})
        
        prompt = f"""
        Generate a custom summary based on the user's specific requirements.
        
        Custom Template Requirements:
        {json.dumps(custom_template, indent=2)}
        
        Requested Sections:
        {json.dumps(custom_sections, indent=2)}
        
        Output Format: {output_format}
        
        Source Data:
        Discussion Analysis: {json.dumps(analysis, indent=2)}
        Key Conversation Elements: {self._extract_key_content(conversation_log)}
        
        Follow the user's custom template exactly, ensuring all requested sections 
        are included with the specified format and depth of analysis.
        
        Return the summary in the exact structure requested by the user.
        """
        
        try:
            response = self.llm_client.generate(prompt, max_tokens=5000, temperature=0.3)
            
            if output_format == 'json':
                json_str = self._extract_json_from_response(response, '{', '}')
                summary = json.loads(json_str)
            else:
                summary = {'content': response, 'format': output_format}
            
            # Add metadata
            summary['summary_type'] = 'custom'
            summary['generated_at'] = datetime.now().isoformat()
            summary['summary_id'] = str(uuid.uuid4())
            summary['source_simulation'] = simulation_data.get('simulation_id')
            summary['custom_schema_used'] = schema
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating custom summary: {e}")
            return self._generate_fallback_summary(simulation_data, "custom")
    
    def _generate_comprehensive_summary(self, simulation_data: Dict[str, Any], 
                                     schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive default summary"""
        
        conversation_log = simulation_data.get('simulation_results', {}).get('conversation_log', [])
        analysis = simulation_data.get('analysis', {})
        metadata = simulation_data.get('metadata', {})
        
        prompt = f"""
        Create a comprehensive focus group summary covering all key aspects.
        
        Simulation Overview:
        - Participants: {simulation_data.get('participants', 0)}
        - Duration: {metadata.get('duration_minutes', 60)} minutes
        - Interactions: {metadata.get('total_interactions', 0)}
        - Spontaneous Moments: {metadata.get('spontaneous_moments', 0)}
        
        Discussion Analysis:
        {json.dumps(analysis, indent=2)}
        
        Key Discussion Content:
        {self._extract_key_content(conversation_log)}
        
        Create a comprehensive summary including:
        
        1. **Session Overview**
           - Research objectives achieved
           - Participant engagement summary
           - Discussion quality assessment
        
        2. **Key Findings**
           - Primary themes identified
           - Participant consensus areas
           - Points of disagreement or debate
        
        3. **Consumer Insights**
           - Behavioral observations
           - Attitude and preference patterns
           - Decision-making factors
        
        4. **Business Intelligence**
           - Market opportunities identified
           - Competitive insights gathered
           - Product/service implications
        
        5. **Recommendations**
           - Strategic recommendations
           - Tactical next steps
           - Further research needs
        
        6. **Supporting Evidence**
           - Key quotes and examples
           - Quantitative observations
           - Group dynamic insights
        
        Return as well-structured JSON covering all aspects comprehensively.
        """
        
        try:
            response = self.llm_client.generate(prompt, max_tokens=5000, temperature=0.3)
            json_str = self._extract_json_from_response(response, '{', '}')
            summary = json.loads(json_str)
            
            # Add metadata
            summary['summary_type'] = 'comprehensive'
            summary['generated_at'] = datetime.now().isoformat()
            summary['summary_id'] = str(uuid.uuid4())
            summary['source_simulation'] = simulation_data.get('simulation_id')
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating comprehensive summary: {e}")
            return self._generate_fallback_summary(simulation_data, "comprehensive")
    
    def _extract_key_content(self, conversation_log: List[Dict[str, Any]]) -> List[str]:
        """Extract key content from conversation log"""
        
        key_content = []
        
        for item in conversation_log:
            if item.get('type') in ['participant_response', 'follow_up_response', 'spontaneous_reaction']:
                speaker = item.get('speaker', 'Unknown')
                content = item.get('content', '')
                key_content.append(f"{speaker}: {content}")
        
        # Limit to most relevant content
        return key_content[:20]  # Top 20 most relevant exchanges
    
    def _extract_themes_from_conversation(self, conversation_log: List[Dict[str, Any]]) -> str:
        """Extract themes from conversation for analysis"""
        
        participant_content = [
            item['content'] for item in conversation_log 
            if item.get('type') in ['participant_response', 'follow_up_response']
        ]
        
        if not participant_content:
            return "No participant content available"
        
        # Combine and summarize themes
        combined_content = " ".join(participant_content[:10])  # Limit for token management
        
        return combined_content[:2000]  # Truncate for prompt efficiency
    
    def _generate_fallback_summary(self, simulation_data: Dict[str, Any], 
                                 summary_type: str) -> Dict[str, Any]:
        """Generate basic fallback summary when main generation fails"""
        
        return {
            'summary_type': summary_type,
            'summary_id': str(uuid.uuid4()),
            'generated_at': datetime.now().isoformat(),
            'source_simulation': simulation_data.get('simulation_id'),
            'status': 'fallback_generated',
            'content': {
                'overview': f"Focus group completed with {simulation_data.get('participants', 0)} participants",
                'key_findings': [
                    "Discussion completed successfully",
                    "Participant engagement observed",
                    "Multiple perspectives captured"
                ],
                'recommendations': [
                    "Review raw discussion content",
                    "Conduct manual analysis",
                    "Consider follow-up research"
                ],
                'note': f"Automated {summary_type} summary generation encountered technical difficulties. Please review the raw simulation data for detailed insights."
            }
        }
    
    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Get list of available summary templates"""
        
        return [
            {
                'type': 'executive',
                'name': 'Executive Summary',
                'description': 'High-level summary for business stakeholders',
                'sections': ['overview', 'key_findings', 'business_implications', 'recommended_actions']
            },
            {
                'type': 'detailed',
                'name': 'Detailed Report',
                'description': 'Comprehensive analytical report with full methodology',
                'sections': ['methodology', 'participant_profiles', 'discussion_flow', 'insights', 'recommendations']
            },
            {
                'type': 'insights_only',
                'name': 'Insights Summary',
                'description': 'Focus on key insights and actionable intelligence',
                'sections': ['consumer_insights', 'pain_points', 'opportunities', 'recommendations']
            },
            {
                'type': 'comprehensive',
                'name': 'Comprehensive Summary',
                'description': 'Complete overview covering all aspects',
                'sections': ['overview', 'findings', 'insights', 'business_intelligence', 'recommendations']
            },
            {
                'type': 'custom',
                'name': 'Custom Format',
                'description': 'User-defined structure and content',
                'sections': ['user_defined']
            }
        ]