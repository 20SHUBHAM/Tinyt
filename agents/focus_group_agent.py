"""
DynamicFocusGroupAgent - Orchestrates realistic focus group discussions using TinyTroupe
"""

import json
import uuid
import time
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from .base_agent import BaseAgent

# TinyTroupe imports
import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe import control

class DynamicFocusGroupAgent(BaseAgent):
    """Agent responsible for running realistic focus group simulations"""
    
    def __init__(self, config):
        super().__init__(config)
        self.agent_name = "DynamicFocusGroupAgent"
        self.cache_dir = config.tinytroupe_cache_dir
    
    def run_simulation(self, personas: List[Dict[str, Any]], 
                      framework: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Run a complete focus group simulation
        
        Args:
            personas: List of participant personas
            framework: Discussion framework
            session_id: Unique session identifier
            
        Returns:
            Complete simulation results
        """
        
        simulation_id = f"focus_group_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Initialize TinyTroupe session
            cache_file = f"{self.cache_dir}/{simulation_id}.cache.json"
            control.begin(cache_file)
            
            # Create TinyPerson agents from personas
            participants = self._create_tinytroupe_participants(personas)
            
            # Create moderator
            moderator = self._create_moderator(framework)
            
            # Create focus group environment
            focus_group = TinyWorld("Virtual Focus Group Room", participants + [moderator])
            
            # Run simulation phases
            simulation_results = self._execute_discussion_phases(
                participants, moderator, framework, focus_group, simulation_id
            )
            
            # Generate insights and analysis
            analysis = self._analyze_discussion(simulation_results, personas, framework)
            
            # Compile final results
            final_results = {
                'simulation_id': simulation_id,
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'participants': len(participants),
                'framework_used': framework['framework_id'],
                'simulation_results': simulation_results,
                'analysis': analysis,
                'metadata': {
                    'duration_minutes': framework.get('duration_minutes', 60),
                    'phases_completed': len(simulation_results.get('phases', [])),
                    'total_interactions': len(simulation_results.get('conversation_log', [])),
                    'spontaneous_moments': len(simulation_results.get('spontaneous_interactions', []))
                }
            }
            
            return final_results
            
        except Exception as e:
            self.logger.error(f"Error running simulation: {e}")
            return self._generate_error_result(simulation_id, session_id, str(e))
        
        finally:
            try:
                control.end()
            except:
                pass
    
    def _create_tinytroupe_participants(self, personas: List[Dict[str, Any]]) -> List[TinyPerson]:
        """Convert persona dictionaries to TinyPerson objects"""
        
        participants = []
        
        for persona in personas:
            try:
                participant = TinyPerson(persona['name'])
                
                # Set basic demographics
                demographics = persona.get('demographics', {})
                participant.define("age", demographics.get('age', 25))
                participant.define("occupation", demographics.get('occupation', 'Professional'))
                participant.define("location", demographics.get('location', 'Urban'))
                
                # Create comprehensive background
                background = self._create_participant_background(persona)
                participant.define("background", background)
                
                participants.append(participant)
                
            except Exception as e:
                self.logger.error(f"Error creating participant {persona.get('name', 'Unknown')}: {e}")
                continue
        
        return participants
    
    def _create_participant_background(self, persona: Dict[str, Any]) -> str:
        """Create comprehensive background description for TinyPerson"""
        
        name = persona.get('name', 'Participant')
        demographics = persona.get('demographics', {})
        psychographics = persona.get('psychographics', {})
        behaviors = persona.get('behaviors', {})
        context_specific = persona.get('context_specific', {})
        discussion_style = persona.get('discussion_style', {})
        background_story = persona.get('background_story', '')
        
        background_parts = []
        
        # Basic identity
        age = demographics.get('age', 'adult')
        occupation = demographics.get('occupation', 'professional')
        location = demographics.get('location', 'urban area')
        
        background_parts.append(f"You are {name}, a {age}-year-old {occupation} from {location}.")
        
        # Personality and values
        traits = psychographics.get('personality_traits', [])
        values = psychographics.get('values', [])
        if traits:
            background_parts.append(f"Your key personality traits are: {', '.join(traits)}.")
        if values:
            background_parts.append(f"You value: {', '.join(values)}.")
        
        # Behavioral patterns
        shopping = behaviors.get('shopping_behavior', '')
        if shopping:
            background_parts.append(f"Your shopping behavior: {shopping}")
        
        # Context-specific details
        budget = context_specific.get('budget_constraints', '')
        pain_points = context_specific.get('pain_points', [])
        goals = context_specific.get('goals', [])
        
        if budget:
            background_parts.append(f"Budget situation: {budget}")
        if pain_points:
            background_parts.append(f"Your main challenges include: {', '.join(pain_points)}.")
        if goals:
            background_parts.append(f"Your goals are: {', '.join(goals)}.")
        
        # Discussion style
        participation = discussion_style.get('participation_level', 'medium')
        tendency = discussion_style.get('agreement_tendency', 'balanced')
        speaking_style = discussion_style.get('speaking_style', 'conversational')
        
        background_parts.append(f"In discussions, you tend to have {participation} participation levels.")
        background_parts.append(f"You are generally {tendency} in your responses to others.")
        background_parts.append(f"Your speaking style is {speaking_style}.")
        
        # Background story
        if background_story:
            background_parts.append(f"Background: {background_story}")
        
        # Conversation instructions
        background_parts.append("""
        In this focus group discussion:
        - Share specific, personal examples and experiences
        - React naturally to what others say
        - Ask questions when curious about others' experiences
        - Express genuine opinions, including disagreement when appropriate
        - Use natural speech patterns and your authentic voice
        - Build on others' comments when they resonate with you
        - Share both positive and negative experiences honestly
        """)
        
        return " ".join(background_parts)
    
    def _create_moderator(self, framework: Dict[str, Any]) -> TinyPerson:
        """Create an expert moderator based on the framework"""
        
        moderator = TinyPerson("Dr. Sarah Chen")
        
        guidelines = framework.get('moderator_guidelines', {})
        opening_strategy = guidelines.get('opening_strategy', 'Professional and welcoming')
        
        moderator_background = f"""
        You are Dr. Sarah Chen, an experienced focus group moderator with 15+ years of experience 
        in consumer research and market analysis. You are skilled at creating comfortable environments 
        where participants feel safe to share honest opinions.
        
        Your moderation style:
        - {opening_strategy}
        - You ask follow-up questions that dig deeper into interesting responses
        - You manage time efficiently while allowing natural conversation flow
        - You ensure all participants have opportunities to contribute
        - You redirect gently when conversations go off-topic
        - You synthesize themes you're hearing and validate with the group
        
        For this session, you will:
        - Follow the structured discussion phases but adapt based on group energy
        - Use the provided questions as starting points, not rigid scripts
        - Encourage specific examples and stories rather than abstract opinions
        - Note interesting conflicts or agreements between participants
        - Keep the discussion focused on actionable business insights
        
        Your communication approach:
        - Use natural, conversational language
        - Show genuine curiosity about participants' experiences
        - Validate all perspectives while probing for deeper insights
        - Use phrases like "That's interesting, tell me more" and "I'm hearing some themes here"
        - Manage dominant speakers politely and encourage quieter participants
        """
        
        moderator.define("background", moderator_background)
        moderator.define("role", "Expert Focus Group Moderator")
        
        return moderator
    
    def _execute_discussion_phases(self, participants: List[TinyPerson], moderator: TinyPerson,
                                 framework: Dict[str, Any], focus_group: TinyWorld,
                                 simulation_id: str) -> Dict[str, Any]:
        """Execute the structured discussion phases"""
        
        phases = framework.get('discussion_phases', [])
        conversation_log = []
        spontaneous_interactions = []
        phase_results = []
        
        self.logger.info(f"Starting simulation {simulation_id} with {len(participants)} participants")
        
        # Pre-discussion setup
        setup_result = self._simulate_pre_discussion(participants, moderator, focus_group)
        conversation_log.extend(setup_result)
        
        # Execute each phase
        for phase_idx, phase in enumerate(phases):
            self.logger.info(f"Executing phase {phase_idx + 1}: {phase.get('name', 'Unnamed Phase')}")
            
            phase_result = self._execute_single_phase(
                phase, participants, moderator, focus_group, phase_idx
            )
            
            phase_results.append(phase_result)
            conversation_log.extend(phase_result['conversation'])
            spontaneous_interactions.extend(phase_result['spontaneous_moments'])
            
            # Add natural transition pause
            if phase_idx < len(phases) - 1:
                transition = self._simulate_phase_transition(moderator, focus_group)
                conversation_log.extend(transition)
        
        # Post-discussion wrap-up
        closing_result = self._simulate_closing(moderator, participants, focus_group, framework)
        conversation_log.extend(closing_result)
        
        return {
            'simulation_id': simulation_id,
            'phases': phase_results,
            'conversation_log': conversation_log,
            'spontaneous_interactions': spontaneous_interactions,
            'participant_interactions': self._analyze_participant_interactions(conversation_log),
            'discussion_dynamics': self._analyze_group_dynamics(conversation_log, participants)
        }
    
    def _simulate_pre_discussion(self, participants: List[TinyPerson], 
                               moderator: TinyPerson, focus_group: TinyWorld) -> List[Dict[str, Any]]:
        """Simulate natural pre-discussion moments"""
        
        pre_discussion = []
        
        # Moderator welcome
        welcome_prompt = """
        Welcome everyone to our focus group session. Before we begin recording, let's take a moment 
        to get settled. Please help yourselves to refreshments, and feel free to chat naturally 
        while everyone arrives.
        """
        
        moderator.listen(welcome_prompt)
        welcome_response = moderator.act()
        
        pre_discussion.append({
            'speaker': 'Dr. Sarah Chen',
            'content': welcome_response,
            'timestamp': datetime.now().isoformat(),
            'type': 'moderator_welcome'
        })
        
        # Natural participant chatter
        for participant in random.sample(participants, min(3, len(participants))):
            casual_prompt = "Make a brief, natural comment as participants are settling in. This could be about the room, refreshments, or a casual greeting to others."
            
            participant.listen(casual_prompt)
            casual_response = participant.act()
            
            if casual_response:
                pre_discussion.append({
                    'speaker': participant.name,
                    'content': casual_response,
                    'timestamp': datetime.now().isoformat(),
                    'type': 'casual_chatter'
                })
        
        return pre_discussion
    
    def _execute_single_phase(self, phase: Dict[str, Any], participants: List[TinyPerson],
                            moderator: TinyPerson, focus_group: TinyWorld, 
                            phase_idx: int) -> Dict[str, Any]:
        """Execute a single discussion phase"""
        
        phase_name = phase.get('name', f'Phase {phase_idx + 1}')
        objective = phase.get('objective', '')
        primary_questions = phase.get('primary_questions', [])
        follow_up_probes = phase.get('follow_up_probes', [])
        
        phase_conversation = []
        spontaneous_moments = []
        
        # Moderator introduces phase
        phase_intro = f"""
        Now let's move into our discussion about {phase_name}. {objective}
        I'd like to start with a question for the group.
        """
        
        moderator.listen(phase_intro)
        intro_response = moderator.act()
        
        phase_conversation.append({
            'speaker': 'Dr. Sarah Chen',
            'content': intro_response,
            'timestamp': datetime.now().isoformat(),
            'type': 'phase_introduction',
            'phase': phase_name
        })
        
        # Process primary questions
        for question_data in primary_questions:
            question = question_data.get('question', '')
            
            # Moderator asks question
            moderator.listen(f"Ask the group: {question}")
            question_response = moderator.act()
            
            phase_conversation.append({
                'speaker': 'Dr. Sarah Chen',
                'content': question_response,
                'timestamp': datetime.now().isoformat(),
                'type': 'primary_question',
                'phase': phase_name
            })
            
            # Participants respond
            response_order = self._determine_response_order(participants)
            
            for participant in response_order:
                # Participant considers and responds
                response_prompt = f"""
                The moderator just asked: "{question}"
                
                Respond naturally based on your background and experience. Share specific examples 
                and personal perspectives. Be authentic to your personality and circumstances.
                """
                
                participant.listen(response_prompt)
                participant_response = participant.act()
                
                if participant_response:
                    phase_conversation.append({
                        'speaker': participant.name,
                        'content': participant_response,
                        'timestamp': datetime.now().isoformat(),
                        'type': 'participant_response',
                        'phase': phase_name,
                        'question': question
                    })
                    
                    # Chance for spontaneous reactions
                    if random.random() > 0.6:  # 40% chance
                        spontaneous = self._generate_spontaneous_reaction(
                            participants, participant, participant_response, focus_group
                        )
                        if spontaneous:
                            spontaneous_moments.append(spontaneous)
                            phase_conversation.append(spontaneous)
            
            # Moderator follow-up based on responses
            if follow_up_probes:
                selected_probe = random.choice(follow_up_probes)
                probe_question = selected_probe.get('probe', '')
                
                follow_up_prompt = f"""
                Based on what you've heard from participants, ask this follow-up: "{probe_question}"
                Adapt it naturally to what participants have actually shared.
                """
                
                moderator.listen(follow_up_prompt)
                follow_up_response = moderator.act()
                
                if follow_up_response:
                    phase_conversation.append({
                        'speaker': 'Dr. Sarah Chen',
                        'content': follow_up_response,
                        'timestamp': datetime.now().isoformat(),
                        'type': 'follow_up_probe',
                        'phase': phase_name
                    })
                    
                    # Select participants to respond to follow-up
                    follow_up_responders = random.sample(participants, min(3, len(participants)))
                    
                    for responder in follow_up_responders:
                        follow_up_participant_prompt = f"""
                        The moderator asked: "{follow_up_response}"
                        Respond if this resonates with your experience or if you have something to add.
                        """
                        
                        responder.listen(follow_up_participant_prompt)
                        follow_up_participant_response = responder.act()
                        
                        if follow_up_participant_response:
                            phase_conversation.append({
                                'speaker': responder.name,
                                'content': follow_up_participant_response,
                                'timestamp': datetime.now().isoformat(),
                                'type': 'follow_up_response',
                                'phase': phase_name
                            })
        
        return {
            'phase_name': phase_name,
            'objective': objective,
            'conversation': phase_conversation,
            'spontaneous_moments': spontaneous_moments,
            'insights_captured': self._extract_phase_insights(phase_conversation)
        }
    
    def _determine_response_order(self, participants: List[TinyPerson]) -> List[TinyPerson]:
        """Determine natural response order based on personality types"""
        
        # Create a weighted random order based on participation tendencies
        eager_responders = []
        moderate_responders = []
        hesitant_responders = []
        
        for participant in participants:
            # This is a simplified categorization
            # In a real implementation, we'd use the persona's discussion_style
            if random.random() < 0.3:  # 30% eager
                eager_responders.append(participant)
            elif random.random() < 0.6:  # 40% moderate (of remaining)
                moderate_responders.append(participant)
            else:  # 30% hesitant
                hesitant_responders.append(participant)
        
        # Randomize within categories but maintain natural flow
        random.shuffle(eager_responders)
        random.shuffle(moderate_responders)
        random.shuffle(hesitant_responders)
        
        # Combine in natural order
        response_order = eager_responders + moderate_responders + hesitant_responders
        
        return response_order
    
    def _generate_spontaneous_reaction(self, participants: List[TinyPerson], 
                                     speaker: TinyPerson, content: str,
                                     focus_group: TinyWorld) -> Optional[Dict[str, Any]]:
        """Generate spontaneous reactions between participants"""
        
        # Select a different participant to react
        potential_reactors = [p for p in participants if p != speaker]
        if not potential_reactors:
            return None
        
        reactor = random.choice(potential_reactors)
        
        reaction_prompt = f"""
        {speaker.name} just shared: "{content}"
        
        You have a spontaneous reaction to this. Respond naturally - you might:
        - Agree enthusiastically and share a similar experience
        - Disagree politely and explain your perspective
        - Ask a clarifying question
        - Build on their point with additional insight
        
        Keep your reaction brief and conversational.
        """
        
        try:
            reactor.listen(reaction_prompt)
            reaction = reactor.act()
            
            if reaction:
                return {
                    'speaker': reactor.name,
                    'content': reaction,
                    'timestamp': datetime.now().isoformat(),
                    'type': 'spontaneous_reaction',
                    'triggered_by': speaker.name,
                    'original_content': content[:100] + "..." if len(content) > 100 else content
                }
        except Exception as e:
            self.logger.warning(f"Error generating spontaneous reaction: {e}")
        
        return None
    
    def _simulate_phase_transition(self, moderator: TinyPerson, 
                                 focus_group: TinyWorld) -> List[Dict[str, Any]]:
        """Simulate natural transitions between phases"""
        
        transition_prompt = """
        Provide a brief, natural transition to the next part of our discussion. 
        You might summarize what you've heard so far or set up the next topic.
        """
        
        moderator.listen(transition_prompt)
        transition_response = moderator.act()
        
        return [{
            'speaker': 'Dr. Sarah Chen',
            'content': transition_response,
            'timestamp': datetime.now().isoformat(),
            'type': 'phase_transition'
        }]
    
    def _simulate_closing(self, moderator: TinyPerson, participants: List[TinyPerson],
                        focus_group: TinyWorld, framework: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Simulate natural session closing"""
        
        closing_conversation = []
        
        # Moderator closing summary
        closing_strategy = framework.get('closing_strategy', {})
        summary_approach = closing_strategy.get('summary_approach', 'Highlight key themes')
        
        closing_prompt = f"""
        We're approaching the end of our session. {summary_approach}
        Thank the participants and ask for any final thoughts.
        """
        
        moderator.listen(closing_prompt)
        closing_response = moderator.act()
        
        closing_conversation.append({
            'speaker': 'Dr. Sarah Chen',
            'content': closing_response,
            'timestamp': datetime.now().isoformat(),
            'type': 'session_closing'
        })
        
        # Final participant comments
        final_responders = random.sample(participants, min(3, len(participants)))
        
        for participant in final_responders:
            final_prompt = """
            The moderator is asking for final thoughts. Share any concluding comments 
            or key takeaways you'd like to emphasize.
            """
            
            participant.listen(final_prompt)
            final_response = participant.act()
            
            if final_response:
                closing_conversation.append({
                    'speaker': participant.name,
                    'content': final_response,
                    'timestamp': datetime.now().isoformat(),
                    'type': 'final_thoughts'
                })
        
        return closing_conversation
    
    def _extract_phase_insights(self, phase_conversation: List[Dict[str, Any]]) -> List[str]:
        """Extract key insights from phase conversation"""
        
        insights = []
        participant_responses = [
            item['content'] for item in phase_conversation 
            if item['type'] in ['participant_response', 'follow_up_response']
        ]
        
        if participant_responses:
            insight_prompt = f"""
            Analyze these participant responses and extract 3-5 key insights:
            
            {json.dumps(participant_responses, indent=2)}
            
            Return insights as a JSON array of strings, focusing on:
            - Common themes and patterns
            - Surprising or unexpected perspectives
            - Actionable business implications
            - Conflicting viewpoints that reveal market segments
            """
            
            try:
                response = self.llm_client.generate(insight_prompt, max_tokens=1000)
                json_str = self._extract_json_from_response(response, '[', ']')
                insights = json.loads(json_str)
            except Exception as e:
                self.logger.warning(f"Error extracting insights: {e}")
                insights = ["Phase completed with participant engagement"]
        
        return insights
    
    def _analyze_participant_interactions(self, conversation_log: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze interactions between participants"""
        
        interactions = {}
        speaker_counts = {}
        
        for item in conversation_log:
            speaker = item.get('speaker', 'Unknown')
            content_type = item.get('type', 'unknown')
            
            # Count contributions by speaker
            if speaker not in speaker_counts:
                speaker_counts[speaker] = 0
            speaker_counts[speaker] += 1
            
            # Track spontaneous reactions
            if content_type == 'spontaneous_reaction':
                triggered_by = item.get('triggered_by', 'Unknown')
                key = f"{speaker} -> {triggered_by}"
                if key not in interactions:
                    interactions[key] = 0
                interactions[key] += 1
        
        return {
            'speaker_contribution_counts': speaker_counts,
            'spontaneous_interactions': interactions,
            'most_active_participant': max(speaker_counts.items(), key=lambda x: x[1])[0] if speaker_counts else None,
            'total_interactions': len(conversation_log)
        }
    
    def _analyze_group_dynamics(self, conversation_log: List[Dict[str, Any]], 
                              participants: List[TinyPerson]) -> Dict[str, Any]:
        """Analyze overall group dynamics"""
        
        participant_names = [p.name for p in participants]
        moderator_interactions = len([item for item in conversation_log if item.get('speaker') == 'Dr. Sarah Chen'])
        participant_interactions = len([item for item in conversation_log if item.get('speaker') in participant_names])
        spontaneous_count = len([item for item in conversation_log if item.get('type') == 'spontaneous_reaction'])
        
        engagement_ratio = participant_interactions / max(moderator_interactions, 1)
        spontaneous_ratio = spontaneous_count / max(participant_interactions, 1)
        
        return {
            'total_exchanges': len(conversation_log),
            'moderator_interventions': moderator_interactions,
            'participant_contributions': participant_interactions,
            'spontaneous_reactions': spontaneous_count,
            'engagement_ratio': round(engagement_ratio, 2),
            'spontaneous_ratio': round(spontaneous_ratio, 2),
            'discussion_quality': 'high' if engagement_ratio > 2 and spontaneous_ratio > 0.2 else 'moderate' if engagement_ratio > 1 else 'low'
        }
    
    def _analyze_discussion(self, simulation_results: Dict[str, Any], 
                          personas: List[Dict[str, Any]], 
                          framework: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive analysis of the discussion"""
        
        conversation_log = simulation_results.get('conversation_log', [])
        
        # Extract all participant content
        participant_content = [
            item['content'] for item in conversation_log 
            if item.get('type') in ['participant_response', 'follow_up_response', 'spontaneous_reaction']
        ]
        
        analysis_prompt = f"""
        Analyze this focus group discussion and provide comprehensive insights:
        
        Discussion Topic: {framework.get('topic', 'General Discussion')}
        Business Context: {framework.get('business_context', 'Market Research')}
        
        Participant Content:
        {json.dumps(participant_content, indent=2)}
        
        Group Dynamics:
        {json.dumps(simulation_results.get('discussion_dynamics', {}), indent=2)}
        
        Provide analysis in the following JSON structure:
        {{
            "key_themes": ["theme1", "theme2", "theme3"],
            "participant_segments": [
                {{
                    "segment_name": "Segment Name",
                    "characteristics": ["char1", "char2"],
                    "key_quotes": ["quote1", "quote2"]
                }}
            ],
            "business_insights": {{
                "opportunities": ["opportunity1", "opportunity2"],
                "challenges": ["challenge1", "challenge2"],
                "recommendations": ["recommendation1", "recommendation2"]
            }},
            "discussion_quality": {{
                "engagement_level": "high/medium/low",
                "authenticity_markers": ["marker1", "marker2"],
                "group_dynamics_summary": "description"
            }},
            "actionable_takeaways": ["takeaway1", "takeaway2", "takeaway3"]
        }}
        
        Focus on insights that are specific, actionable, and backed by evidence from the discussion.
        """
        
        try:
            response = self.llm_client.generate(analysis_prompt, max_tokens=3000)
            json_str = self._extract_json_from_response(response, '{', '}')
            analysis = json.loads(json_str)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing discussion: {e}")
            return {
                "key_themes": ["Discussion completed"],
                "participant_segments": [],
                "business_insights": {
                    "opportunities": ["Further analysis needed"],
                    "challenges": ["Analysis error occurred"],
                    "recommendations": ["Review raw discussion content"]
                },
                "discussion_quality": {
                    "engagement_level": "unknown",
                    "authenticity_markers": [],
                    "group_dynamics_summary": "Analysis unavailable"
                },
                "actionable_takeaways": ["Review simulation results manually"]
            }
    
    def _generate_error_result(self, simulation_id: str, session_id: str, error_message: str) -> Dict[str, Any]:
        """Generate error result when simulation fails"""
        
        return {
            'simulation_id': simulation_id,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error_message': error_message,
            'simulation_results': {
                'phases': [],
                'conversation_log': [
                    {
                        'speaker': 'System',
                        'content': f'Simulation failed: {error_message}',
                        'timestamp': datetime.now().isoformat(),
                        'type': 'error'
                    }
                ],
                'spontaneous_interactions': [],
                'participant_interactions': {},
                'discussion_dynamics': {}
            },
            'analysis': {
                'key_themes': ['Simulation error'],
                'participant_segments': [],
                'business_insights': {
                    'opportunities': [],
                    'challenges': ['Technical difficulties'],
                    'recommendations': ['Retry simulation with adjusted parameters']
                },
                'discussion_quality': {
                    'engagement_level': 'error',
                    'authenticity_markers': [],
                    'group_dynamics_summary': 'Simulation failed to complete'
                },
                'actionable_takeaways': ['Technical issue needs resolution']
            },
            'metadata': {
                'duration_minutes': 0,
                'phases_completed': 0,
                'total_interactions': 0,
                'spontaneous_moments': 0
            }
        }