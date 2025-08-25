"""
QAAssistantAgent - Interactive Q&A about focus group discussions
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class QAAssistantAgent(BaseAgent):
    """Agent responsible for answering questions about focus group discussions"""
    
    def __init__(self, config):
        super().__init__(config)
        self.agent_name = "QAAssistantAgent"
    
    def answer_question(self, simulation_data: Dict[str, Any], question: str) -> Dict[str, Any]:
        """
        Answer a specific question about the focus group discussion
        
        Args:
            simulation_data: Complete simulation results
            question: User's question
            
        Returns:
            Structured answer with supporting evidence
        """
        
        # Determine question type for targeted response
        question_type = self._classify_question(question)
        
        conversation_log = simulation_data.get('simulation_results', {}).get('conversation_log', [])
        analysis = simulation_data.get('analysis', {})
        
        # Extract relevant context based on question type
        relevant_context = self._extract_relevant_context(
            conversation_log, analysis, question, question_type
        )
        
        prompt = f"""
        You are an expert focus group analyst. Answer this specific question about the discussion:
        
        Question: "{question}"
        
        Question Type: {question_type}
        
        Discussion Context:
        {json.dumps(relevant_context, indent=2)}
        
        Complete Analysis:
        {json.dumps(analysis, indent=2)}
        
        Provide a comprehensive answer that:
        1. Directly addresses the question
        2. Provides specific evidence from the discussion
        3. Includes relevant quotes when available
        4. Offers interpretation and context
        5. Suggests implications or next steps if relevant
        
        Structure your response as JSON:
        {{
            "question": "the original question",
            "direct_answer": "clear, direct response",
            "supporting_evidence": [
                {{
                    "type": "quote/observation/data",
                    "content": "specific evidence",
                    "source": "participant name or analysis section"
                }}
            ],
            "interpretation": "what this means in context",
            "implications": ["implication1", "implication2"],
            "related_insights": ["related finding1", "related finding2"],
            "confidence_level": "high/medium/low",
            "follow_up_questions": ["suggested question1", "suggested question2"]
        }}
        
        Be specific, evidence-based, and actionable in your response.
        """
        
        try:
            response = self.llm_client.generate(prompt, max_tokens=2000, temperature=0.3)
            json_str = self._extract_json_from_response(response, '{', '}')
            answer = json.loads(json_str)
            
            # Add metadata
            answer['answer_id'] = str(uuid.uuid4())
            answer['generated_at'] = datetime.now().isoformat()
            answer['source_simulation'] = simulation_data.get('simulation_id')
            answer['question_type'] = question_type
            
            return answer
            
        except Exception as e:
            self.logger.error(f"Error answering question: {e}")
            return self._generate_fallback_answer(question, str(e))
    
    def suggest_questions(self, simulation_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Suggest relevant questions based on the discussion content
        
        Args:
            simulation_data: Complete simulation results
            
        Returns:
            List of suggested questions with context
        """
        
        analysis = simulation_data.get('analysis', {})
        conversation_log = simulation_data.get('simulation_results', {}).get('conversation_log', [])
        dynamics = simulation_data.get('simulation_results', {}).get('discussion_dynamics', {})
        
        # Extract interesting patterns for question generation
        key_themes = analysis.get('key_themes', [])
        business_insights = analysis.get('business_insights', {})
        spontaneous_interactions = simulation_data.get('simulation_results', {}).get('spontaneous_interactions', [])
        
        prompt = f"""
        Based on this focus group discussion, suggest insightful questions that would help 
        stakeholders understand the findings better.
        
        Key Themes Identified:
        {json.dumps(key_themes, indent=2)}
        
        Business Insights:
        {json.dumps(business_insights, indent=2)}
        
        Discussion Dynamics:
        {json.dumps(dynamics, indent=2)}
        
        Spontaneous Interactions: {len(spontaneous_interactions)}
        
        Generate 8-12 diverse questions across these categories:
        
        1. **Insight Clarification** (2-3 questions)
           - Questions that dig deeper into key findings
           - Help clarify surprising or unexpected results
        
        2. **Business Application** (2-3 questions)
           - How findings translate to business strategy
           - Implementation and action-oriented questions
        
        3. **Participant Comparison** (2-3 questions)
           - Compare different participant perspectives
           - Explore segment differences
        
        4. **Process Understanding** (2-3 questions)
           - Questions about how participants think/decide
           - Workflow and experience-related queries
        
        5. **Future Implications** (1-2 questions)
           - Forward-looking strategic questions
           - Trend and evolution questions
        
        Return as JSON array:
        [
            {{
                "question": "specific question text",
                "category": "insight_clarification/business_application/participant_comparison/process_understanding/future_implications",
                "rationale": "why this question is valuable",
                "expected_insights": "what this question might reveal",
                "difficulty": "basic/intermediate/advanced"
            }}
        ]
        
        Make questions specific, actionable, and relevant to the actual discussion content.
        """
        
        try:
            response = self.llm_client.generate(prompt, max_tokens=3000, temperature=0.4)
            json_str = self._extract_json_from_response(response, '[', ']')
            suggestions = json.loads(json_str)
            
            # Add metadata to each suggestion
            for suggestion in suggestions:
                suggestion['suggestion_id'] = str(uuid.uuid4())
                suggestion['generated_at'] = datetime.now().isoformat()
                suggestion['source_simulation'] = simulation_data.get('simulation_id')
            
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Error generating question suggestions: {e}")
            return self._generate_fallback_suggestions()
    
    def analyze_patterns(self, simulation_data: Dict[str, Any], 
                        focus_area: str) -> Dict[str, Any]:
        """
        Analyze specific patterns in the discussion
        
        Args:
            simulation_data: Complete simulation results
            focus_area: Specific area to analyze (e.g., 'disagreements', 'consensus', 'emotions')
            
        Returns:
            Detailed pattern analysis
        """
        
        conversation_log = simulation_data.get('simulation_results', {}).get('conversation_log', [])
        analysis = simulation_data.get('analysis', {})
        
        if focus_area == 'disagreements':
            return self._analyze_disagreement_patterns(conversation_log, analysis)
        elif focus_area == 'consensus':
            return self._analyze_consensus_patterns(conversation_log, analysis)
        elif focus_area == 'emotions':
            return self._analyze_emotional_patterns(conversation_log, analysis)
        elif focus_area == 'participation':
            return self._analyze_participation_patterns(conversation_log, analysis)
        else:
            return self._analyze_general_patterns(conversation_log, analysis, focus_area)
    
    def compare_participants(self, simulation_data: Dict[str, Any], 
                           participant_names: List[str]) -> Dict[str, Any]:
        """
        Compare specific participants' perspectives and contributions
        
        Args:
            simulation_data: Complete simulation results
            participant_names: Names of participants to compare
            
        Returns:
            Detailed comparison analysis
        """
        
        conversation_log = simulation_data.get('simulation_results', {}).get('conversation_log', [])
        
        # Extract content for each participant
        participant_content = {}
        for participant in participant_names:
            participant_content[participant] = [
                item['content'] for item in conversation_log 
                if item.get('speaker') == participant and 
                item.get('type') in ['participant_response', 'follow_up_response', 'spontaneous_reaction']
            ]
        
        prompt = f"""
        Compare these participants based on their contributions to the focus group discussion:
        
        Participants to Compare: {participant_names}
        
        Participant Content:
        {json.dumps(participant_content, indent=2)}
        
        Provide a detailed comparison covering:
        
        1. **Communication Styles**
           - How each participant expresses themselves
           - Formality level and vocabulary choices
           - Conversation patterns
        
        2. **Perspective Differences**
           - Key areas where they agree/disagree
           - Different priorities or values expressed
           - Unique viewpoints each brings
        
        3. **Engagement Patterns**
           - Level of participation
           - Types of contributions (questions, agreements, challenges)
           - Leadership vs. following behaviors
        
        4. **Content Analysis**
           - Main themes each participant focused on
           - Specific insights each provided
           - Examples and experiences shared
        
        5. **Influence Dynamics**
           - How they influenced others' responses
           - Who they responded to most
           - Moments of persuasion or conflict
        
        Return as structured JSON with clear comparisons and specific examples.
        """
        
        try:
            response = self.llm_client.generate(prompt, max_tokens=3000, temperature=0.3)
            json_str = self._extract_json_from_response(response, '{', '}')
            comparison = json.loads(json_str)
            
            # Add metadata
            comparison['comparison_id'] = str(uuid.uuid4())
            comparison['generated_at'] = datetime.now().isoformat()
            comparison['participants_compared'] = participant_names
            comparison['source_simulation'] = simulation_data.get('simulation_id')
            
            return comparison
            
        except Exception as e:
            self.logger.error(f"Error comparing participants: {e}")
            return {
                'error': f'Comparison failed: {str(e)}',
                'participants_compared': participant_names,
                'generated_at': datetime.now().isoformat()
            }
    
    def _classify_question(self, question: str) -> str:
        """Classify the type of question being asked"""
        
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['why', 'reason', 'motivation', 'cause']):
            return 'explanation'
        elif any(word in question_lower for word in ['how many', 'how much', 'count', 'percentage']):
            return 'quantitative'
        elif any(word in question_lower for word in ['what', 'which', 'who']):
            return 'factual'
        elif any(word in question_lower for word in ['compare', 'difference', 'similar', 'contrast']):
            return 'comparison'
        elif any(word in question_lower for word in ['recommend', 'suggest', 'should', 'action']):
            return 'recommendation'
        elif any(word in question_lower for word in ['trend', 'pattern', 'theme', 'insight']):
            return 'pattern_analysis'
        else:
            return 'general'
    
    def _extract_relevant_context(self, conversation_log: List[Dict[str, Any]], 
                                analysis: Dict[str, Any], question: str, 
                                question_type: str) -> Dict[str, Any]:
        """Extract context relevant to the specific question"""
        
        relevant_context = {
            'conversation_excerpts': [],
            'analysis_sections': {},
            'participant_interactions': []
        }
        
        # Extract relevant conversation excerpts based on question keywords
        question_keywords = self._extract_keywords(question)
        
        for item in conversation_log:
            if item.get('type') in ['participant_response', 'follow_up_response', 'spontaneous_reaction']:
                content = item.get('content', '').lower()
                if any(keyword in content for keyword in question_keywords):
                    relevant_context['conversation_excerpts'].append({
                        'speaker': item.get('speaker'),
                        'content': item.get('content'),
                        'type': item.get('type')
                    })
        
        # Include relevant analysis sections
        relevant_context['analysis_sections'] = analysis
        
        # Limit context size for token management
        relevant_context['conversation_excerpts'] = relevant_context['conversation_excerpts'][:10]
        
        return relevant_context
    
    def _extract_keywords(self, question: str) -> List[str]:
        """Extract keywords from question for context matching"""
        
        # Simple keyword extraction (could be enhanced with NLP)
        common_words = {'what', 'how', 'why', 'when', 'where', 'who', 'the', 'a', 'an', 'and', 'or', 'but'}
        
        words = question.lower().split()
        keywords = [word.strip('.,!?;:') for word in words if word not in common_words and len(word) > 2]
        
        return keywords[:5]  # Top 5 keywords
    
    def _analyze_disagreement_patterns(self, conversation_log: List[Dict[str, Any]], 
                                     analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns of disagreement in the discussion"""
        
        disagreements = []
        
        for item in conversation_log:
            content = item.get('content', '').lower()
            if any(phrase in content for phrase in ['disagree', 'but', 'however', 'actually', "i don't think"]):
                disagreements.append(item)
        
        return {
            'pattern_type': 'disagreements',
            'instances_found': len(disagreements),
            'examples': disagreements[:5],
            'analysis': 'Analysis of disagreement patterns in the discussion'
        }
    
    def _analyze_consensus_patterns(self, conversation_log: List[Dict[str, Any]], 
                                  analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns of consensus in the discussion"""
        
        consensus = []
        
        for item in conversation_log:
            content = item.get('content', '').lower()
            if any(phrase in content for phrase in ['agree', 'exactly', 'yes', 'same', 'totally']):
                consensus.append(item)
        
        return {
            'pattern_type': 'consensus',
            'instances_found': len(consensus),
            'examples': consensus[:5],
            'analysis': 'Analysis of consensus patterns in the discussion'
        }
    
    def _analyze_emotional_patterns(self, conversation_log: List[Dict[str, Any]], 
                                  analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze emotional patterns in the discussion"""
        
        emotional_markers = []
        
        emotion_words = ['excited', 'frustrated', 'happy', 'annoyed', 'love', 'hate', 'amazing', 'terrible']
        
        for item in conversation_log:
            content = item.get('content', '').lower()
            if any(emotion in content for emotion in emotion_words):
                emotional_markers.append(item)
        
        return {
            'pattern_type': 'emotions',
            'instances_found': len(emotional_markers),
            'examples': emotional_markers[:5],
            'analysis': 'Analysis of emotional expressions in the discussion'
        }
    
    def _analyze_participation_patterns(self, conversation_log: List[Dict[str, Any]], 
                                      analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze participation patterns in the discussion"""
        
        participation_counts = {}
        
        for item in conversation_log:
            if item.get('type') in ['participant_response', 'follow_up_response', 'spontaneous_reaction']:
                speaker = item.get('speaker', 'Unknown')
                participation_counts[speaker] = participation_counts.get(speaker, 0) + 1
        
        return {
            'pattern_type': 'participation',
            'participation_counts': participation_counts,
            'most_active': max(participation_counts.items(), key=lambda x: x[1]) if participation_counts else None,
            'least_active': min(participation_counts.items(), key=lambda x: x[1]) if participation_counts else None,
            'analysis': 'Analysis of participation levels across participants'
        }
    
    def _analyze_general_patterns(self, conversation_log: List[Dict[str, Any]], 
                                analysis: Dict[str, Any], focus_area: str) -> Dict[str, Any]:
        """Analyze general patterns based on focus area"""
        
        return {
            'pattern_type': focus_area,
            'analysis': f'General pattern analysis for {focus_area}',
            'note': 'This is a placeholder for custom pattern analysis'
        }
    
    def _generate_fallback_answer(self, question: str, error_message: str) -> Dict[str, Any]:
        """Generate fallback answer when main processing fails"""
        
        return {
            'question': question,
            'direct_answer': 'Unable to process question due to technical error',
            'supporting_evidence': [],
            'interpretation': f'Error occurred: {error_message}',
            'implications': ['Manual review of discussion data recommended'],
            'related_insights': [],
            'confidence_level': 'low',
            'follow_up_questions': ['Please rephrase the question', 'Try a more specific question'],
            'answer_id': str(uuid.uuid4()),
            'generated_at': datetime.now().isoformat(),
            'status': 'error'
        }
    
    def _generate_fallback_suggestions(self) -> List[Dict[str, Any]]:
        """Generate fallback question suggestions"""
        
        return [
            {
                'question': 'What were the main themes discussed?',
                'category': 'insight_clarification',
                'rationale': 'Understanding core discussion themes',
                'expected_insights': 'Key focus areas and priorities',
                'difficulty': 'basic',
                'suggestion_id': str(uuid.uuid4()),
                'generated_at': datetime.now().isoformat()
            },
            {
                'question': 'Which participants were most engaged?',
                'category': 'participant_comparison',
                'rationale': 'Understanding participation patterns',
                'expected_insights': 'Engagement levels and dynamics',
                'difficulty': 'basic',
                'suggestion_id': str(uuid.uuid4()),
                'generated_at': datetime.now().isoformat()
            },
            {
                'question': 'What actionable insights emerged?',
                'category': 'business_application',
                'rationale': 'Identifying implementable findings',
                'expected_insights': 'Practical next steps',
                'difficulty': 'intermediate',
                'suggestion_id': str(uuid.uuid4()),
                'generated_at': datetime.now().isoformat()
            }
        ]