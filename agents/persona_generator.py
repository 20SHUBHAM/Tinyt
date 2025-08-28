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
        
        # Simpler, robust format: one persona per line, pipe-delimited, easy to parse
        prompt = f"""
Create {num_personas} diverse consumer personas for: "{description}".

Return ONLY {num_personas} lines using this exact pipe-delimited format (no extra text):
- Name | age | occupation | location | traits: trait1, trait2, trait3 | style: speaking style | story: one sentence background
"""
        
        try:
            # Use simple text generation, then parse lines
            response = self.llm_client.generate(prompt, max_tokens=800, temperature=0.6)
            
            if not response or not isinstance(response, str):
                self.logger.error("Persona generation returned empty response")
                return self._generate_fallback_personas(description, num_personas)
            
            personas = self._parse_pipe_personas(response, num_personas, description)
            if not personas:
                return self._generate_fallback_personas(description, num_personas)
            return personas
            
        except json.JSONDecodeError as e:
            # Not using JSON format for main generation; treat as generic error
            self.logger.error(f"Failed to parse persona JSON: {e}")
            return self._generate_fallback_personas(description, num_personas)
        except Exception as e:
            self.logger.error(f"Error generating personas: {e}")
            return self._generate_fallback_personas(description, num_personas)

    def _parse_pipe_personas(self, text: str, num_personas: int, description: str) -> List[Dict[str, Any]]:
        """Parse pipe-delimited personas from LLM text into full persona dicts."""
        lines = [l.strip() for l in text.splitlines() if l.strip() and l.strip().startswith('-')]
        personas: List[Dict[str, Any]] = []
        for line in lines:
            # Remove leading dash and any bullets
            if line.startswith('-'):
                line = line[1:].strip()
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 4:
                continue
            name = parts[0]
            age_str = parts[1]
            occupation = parts[2]
            location = parts[3]
            traits_part = next((p for p in parts if p.lower().startswith('traits:')), '')
            style_part = next((p for p in parts if p.lower().startswith('style:')), '')
            story_part = next((p for p in parts if p.lower().startswith('story:')), '')

            try:
                age = int(''.join([c for c in age_str if c.isdigit()]) or 0) or 28
            except Exception:
                age = 28

            traits_list = []
            if traits_part:
                traits_list = [t.strip() for t in traits_part.split(':', 1)[-1].split(',') if t.strip()]
            speaking_style = style_part.split(':', 1)[-1].strip() if style_part else 'Conversational'
            story = story_part.split(':', 1)[-1].strip() if story_part else f"Interested in {description}"

            personas.append({
                "id": str(uuid.uuid4()),
                "name": name or "Participant",
                "demographics": {
                    "age": age,
                    "gender": "diverse",
                    "location": location or "Various",
                    "occupation": occupation or "Professional",
                    "income_level": "moderate"
                },
                "psychographics": {
                    "personality_traits": traits_list or ["curious", "thoughtful"],
                    "values": ["authenticity", "value"],
                    "lifestyle": "Modern lifestyle",
                    "communication_style": "Direct and honest",
                    "decision_making": "Research-based"
                },
                "behaviors": {
                    "shopping_behavior": "Online and offline mix",
                    "brand_preferences": "Quality-focused",
                    "technology_usage": "Regular user",
                    "social_media": "Active",
                    "information_sources": ["online", "friends"]
                },
                "context_specific": {
                    "pain_points": ["budget constraints"],
                    "goals": ["good value"],
                    "budget_constraints": "Moderate budget",
                    "experience_level": "intermediate",
                    "preferences": "Practical"
                },
                "discussion_style": {
                    "participation_level": "medium",
                    "agreement_tendency": "balanced",
                    "leadership_style": "collaborative",
                    "interruption_pattern": "occasional",
                    "confidence_level": "medium",
                    "speaking_style": speaking_style
                },
                "background_story": story
            })

            if len(personas) >= num_personas:
                break

        # If fewer than requested, top up with fallbacks
        while len(personas) < num_personas:
            personas.append(self._generate_fallback_personas(description, 1)[0])

        return personas
    
    def generate_quick_personas(self, description: str, num_personas: int = 6) -> List[Dict[str, Any]]:
        """
        Generate personas quickly using a simplified prompt
        
        Args:
            description: Free-text description of target audience
            num_personas: Number of personas to generate
            
        Returns:
            List of basic persona dictionaries
        """
        
        quick_prompt = f"""Create {num_personas} simple personas for "{description}".

Return JSON array:
[{{
  "id": "1",
  "name": "Name",
  "demographics": {{"age": 25, "occupation": "Job", "location": "City"}},
  "personality_traits": ["trait1", "trait2"],
  "background_story": "Brief background"
}}]

Make them diverse and realistic."""
        
        try:
            response = self.llm_client.generate(quick_prompt, max_tokens=1000, temperature=0.8)
            json_str = self._extract_json_from_response(response, '[', ']')
            personas = json.loads(json_str)
            
            # Expand simple personas to full structure
            return self._expand_simple_personas(personas, description)
            
        except Exception as e:
            self.logger.error(f"Quick generation failed: {e}")
            return self._generate_fallback_personas(description, num_personas)
    
    def _expand_simple_personas(self, simple_personas: List[Dict], description: str) -> List[Dict[str, Any]]:
        """Expand simple personas to full structure"""
        
        expanded = []
        for persona in simple_personas:
            expanded_persona = {
                "id": str(uuid.uuid4()),
                "name": persona.get("name", "Participant"),
                "demographics": {
                    "age": persona.get("demographics", {}).get("age", 25),
                    "gender": "diverse",
                    "location": persona.get("demographics", {}).get("location", "Urban"),
                    "occupation": persona.get("demographics", {}).get("occupation", "Professional"),
                    "income_level": "moderate"
                },
                "psychographics": {
                    "personality_traits": persona.get("personality_traits", ["curious", "thoughtful"]),
                    "values": ["authenticity", "value"],
                    "lifestyle": "Modern lifestyle",
                    "communication_style": "Direct and honest",
                    "decision_making": "Research-based"
                },
                "behaviors": {
                    "shopping_behavior": "Online and offline mix",
                    "brand_preferences": "Quality-focused",
                    "technology_usage": "Regular user",
                    "social_media": "Active",
                    "information_sources": ["online", "friends"]
                },
                "context_specific": {
                    "pain_points": ["budget constraints"],
                    "goals": ["good value"],
                    "budget_constraints": "Moderate budget",
                    "experience_level": "intermediate",
                    "preferences": "Practical"
                },
                "discussion_style": {
                    "participation_level": "medium",
                    "agreement_tendency": "balanced",
                    "leadership_style": "collaborative",
                    "interruption_pattern": "occasional",
                    "confidence_level": "medium",
                    "speaking_style": "Conversational"
                },
                "background_story": persona.get("background_story", f"Interested in {description}")
            }
            expanded.append(expanded_persona)
        
        return expanded

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