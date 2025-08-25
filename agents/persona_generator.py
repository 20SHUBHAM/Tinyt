"""
PersonaGeneratorAgent - Generates detailed, diverse personas from free-text descriptions
"""

import json
import uuid
from typing import List, Dict, Any
from .base_agent import BaseAgent

class PersonaGeneratorAgent(BaseAgent):
    """Agent responsible for generating dynamic personas from user descriptions"""
    
    def __init__(self, config):
        super().__init__(config)
        self.agent_name = "PersonaGeneratorAgent"
    
    def generate_personas(self, description: str, num_personas: int = 6) -> List[Dict[str, Any]]:
        """
        Generate diverse personas based on free-text description
        
        Args:
            description: Free-text description of target audience
            num_personas: Number of personas to generate
            
        Returns:
            List of detailed persona dictionaries
        """
        
        prompt = f"""
        You are an expert market researcher and persona generator. Create {num_personas} detailed, diverse personas based on this description:
        
        "{description}"
        
        For each persona, generate a comprehensive profile that includes:
        
        1. **Basic Demographics**:
           - Name (realistic, culturally appropriate)
           - Age
           - Gender
           - Location (city/region)
           - Occupation
           - Income level/spending power
        
        2. **Psychographic Profile**:
           - Personality traits (3-4 key traits)
           - Values and motivations
           - Lifestyle characteristics
           - Communication style
           - Decision-making patterns
        
        3. **Behavioral Patterns**:
           - Shopping behaviors
           - Brand preferences
           - Technology usage
           - Social media habits
           - Information sources
        
        4. **Context-Specific Details**:
           - Relevant pain points or challenges
           - Goals and aspirations
           - Budget constraints or spending patterns
           - Experience level with the topic
           - Specific preferences or aversions
        
        5. **Discussion Style**:
           - How they participate in group discussions
           - Tendencies to agree/disagree
           - Leadership vs follower characteristics
           - Interruption patterns
           - Speaking confidence level
        
        IMPORTANT REQUIREMENTS:
        - Make personas genuinely diverse across demographics, psychographics, and behaviors
        - Include realistic budget/income constraints that affect behavior
        - Create natural personality conflicts and complementary dynamics
        - Ensure personas have authentic speech patterns and vocabulary
        - Include specific, memorable details that make them feel real
        - Consider different experience levels and engagement styles
        
        Return the personas as a JSON array where each persona has this structure:
        {{
            "id": "unique_id",
            "name": "Full Name",
            "demographics": {{
                "age": number,
                "gender": "string",
                "location": "string",
                "occupation": "string",
                "income_level": "string"
            }},
            "psychographics": {{
                "personality_traits": ["trait1", "trait2", "trait3"],
                "values": ["value1", "value2"],
                "lifestyle": "description",
                "communication_style": "description",
                "decision_making": "description"
            }},
            "behaviors": {{
                "shopping_behavior": "description",
                "brand_preferences": "description",
                "technology_usage": "description",
                "social_media": "description",
                "information_sources": ["source1", "source2"]
            }},
            "context_specific": {{
                "pain_points": ["point1", "point2"],
                "goals": ["goal1", "goal2"],
                "budget_constraints": "description",
                "experience_level": "string",
                "preferences": "description"
            }},
            "discussion_style": {{
                "participation_level": "high/medium/low",
                "agreement_tendency": "agreeable/neutral/contrarian",
                "leadership_style": "leader/follower/balanced",
                "interruption_pattern": "frequent/occasional/rare",
                "confidence_level": "high/medium/low",
                "speaking_style": "description"
            }},
            "background_story": "A brief narrative that brings this persona to life"
        }}
        
        Make sure each persona feels like a real person with authentic motivations, constraints, and quirks.
        """
        
        try:
            response = self.llm_client.generate(prompt)
            
            # Extract JSON from response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No valid JSON array found in response")
            
            json_str = response[json_start:json_end]
            personas = json.loads(json_str)
            
            # Add unique IDs if not present
            for persona in personas:
                if 'id' not in persona:
                    persona['id'] = str(uuid.uuid4())
            
            return personas
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse persona JSON: {e}")
            # Return fallback personas
            return self._generate_fallback_personas(description, num_personas)
        
        except Exception as e:
            self.logger.error(f"Error generating personas: {e}")
            return self._generate_fallback_personas(description, num_personas)
    
    def _generate_fallback_personas(self, description: str, num_personas: int) -> List[Dict[str, Any]]:
        """Generate basic fallback personas if main generation fails"""
        
        fallback_personas = []
        
        for i in range(num_personas):
            persona = {
                "id": str(uuid.uuid4()),
                "name": f"Participant {i+1}",
                "demographics": {
                    "age": 20 + (i * 5),
                    "gender": "diverse",
                    "location": "Various",
                    "occupation": "Student/Professional",
                    "income_level": "Variable"
                },
                "psychographics": {
                    "personality_traits": ["curious", "thoughtful"],
                    "values": ["authenticity", "value"],
                    "lifestyle": "Modern, connected",
                    "communication_style": "Direct and honest",
                    "decision_making": "Research-based"
                },
                "behaviors": {
                    "shopping_behavior": "Online and offline mix",
                    "brand_preferences": "Quality-focused",
                    "technology_usage": "Regular user",
                    "social_media": "Active on multiple platforms",
                    "information_sources": ["online reviews", "friends"]
                },
                "context_specific": {
                    "pain_points": ["budget constraints", "choice overload"],
                    "goals": ["find good value", "make informed decisions"],
                    "budget_constraints": "Moderate budget awareness",
                    "experience_level": "intermediate",
                    "preferences": "Practical and reliable"
                },
                "discussion_style": {
                    "participation_level": "medium",
                    "agreement_tendency": "balanced",
                    "leadership_style": "collaborative",
                    "interruption_pattern": "occasional",
                    "confidence_level": "medium",
                    "speaking_style": "Thoughtful and measured"
                },
                "background_story": f"A representative participant interested in {description}"
            }
            
            fallback_personas.append(persona)
        
        return fallback_personas
    
    def refine_persona(self, persona: Dict[str, Any], refinement_notes: str) -> Dict[str, Any]:
        """
        Refine an existing persona based on user feedback
        
        Args:
            persona: Existing persona dictionary
            refinement_notes: User's refinement instructions
            
        Returns:
            Updated persona dictionary
        """
        
        prompt = f"""
        You are refining an existing persona based on user feedback. Here is the current persona:
        
        {json.dumps(persona, indent=2)}
        
        User refinement notes:
        "{refinement_notes}"
        
        Please update the persona to incorporate the user's feedback while maintaining internal consistency.
        Keep all the existing structure but modify the relevant fields based on the refinement notes.
        
        Return the updated persona as JSON with the same structure.
        """
        
        try:
            response = self.llm_client.generate(prompt)
            
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No valid JSON found in response")
            
            json_str = response[json_start:json_end]
            refined_persona = json.loads(json_str)
            
            # Ensure ID is preserved
            refined_persona['id'] = persona['id']
            
            return refined_persona
            
        except Exception as e:
            self.logger.error(f"Error refining persona: {e}")
            return persona  # Return original if refinement fails