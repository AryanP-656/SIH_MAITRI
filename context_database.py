"""
Context Database for MAITRI - Psychological and Astronomy Data
This module contains a knowledge base of psychological and astronomy information
that can be retrieved based on user input for Gemini API context.
"""

import json
from typing import List, Dict, Any
from dataclasses import dataclass
import re

@dataclass
class ContextItem:
    """Represents a single piece of context information"""
    category: str  # 'psychological' or 'astronomy'
    subcategory: str  # e.g., 'stress_management', 'sleep_health', 'space_environment'
    title: str
    content: str
    keywords: List[str]  # Keywords for matching
    priority: int  # 1-5, higher = more important

class ContextDatabase:
    """Manages the context database and retrieval"""
    
    def __init__(self):
        self.context_items = []
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the database with psychological and astronomy data"""
        
        # Psychological Context Data
        psychological_data = [
            {
                "category": "psychological",
                "subcategory": "stress_management",
                "title": "Stress Recognition in Space",
                "content": "Astronauts experience unique stressors including isolation, confinement, and mission pressure. Signs include increased heart rate, sleep disturbances, and changes in communication patterns. Early recognition is crucial for mission success.",
                "keywords": ["stress", "pressure", "anxiety", "overwhelmed", "tension", "worry", "down", "sad", "depressed", "low", "mood", "angry", "anger", "mad", "furious", "irritated", "frustrated"],
                "priority": 5
            },
            {
                "category": "psychological",
                "subcategory": "sleep_health",
                "title": "Sleep Disruption in Space",
                "content": "Space environment disrupts circadian rhythms due to 16 sunrises/sunsets per day. Sleep quality affects cognitive performance, mood, and decision-making. Maintaining regular sleep schedules is critical for astronaut well-being.",
                "keywords": ["sleep", "insomnia", "tired", "fatigue", "exhausted", "rest", "circadian", "can't sleep", "sleepless", "awake"],
                "priority": 4
            },
            {
                "category": "psychological",
                "subcategory": "isolation_effects",
                "title": "Isolation and Confinement Effects",
                "content": "Long-duration space missions create psychological challenges including social isolation, sensory deprivation, and limited personal space. These can lead to mood changes, irritability, and decreased motivation.",
                "keywords": ["isolation", "lonely", "alone", "confined", "trapped", "social", "connection"],
                "priority": 4
            },
            {
                "category": "psychological",
                "subcategory": "coping_strategies",
                "title": "Space-Adapted Coping Strategies",
                "content": "Effective coping strategies for astronauts include mindfulness exercises, virtual reality relaxation, music therapy, exercise routines, and maintaining communication with Earth. Personal hobbies and creative activities help maintain mental health.",
                "keywords": ["coping", "relaxation", "mindfulness", "exercise", "hobbies", "therapy", "meditation"],
                "priority": 3
            },
            {
                "category": "psychological",
                "subcategory": "team_dynamics",
                "title": "Crew Team Dynamics",
                "content": "Small crew environments require excellent communication, conflict resolution, and mutual support. Team cohesion directly impacts mission success and individual psychological well-being.",
                "keywords": ["team", "crew", "communication", "conflict", "support", "cooperation", "relationships"],
                "priority": 3
            },
            {
                "category": "astronomy",
                "subcategory": "nutrition_health",
                "title": "Nutrition and Health in Space",
                "content": "Space nutrition is critical for astronaut health and performance. Food must be specially prepared for microgravity, and proper nutrition helps maintain physical and mental well-being during long missions.",
                "keywords": ["hungry", "food", "nutrition", "eating", "meal", "hunger", "diet", "nutritional"],
                "priority": 3
            }
        ]
        
        # Astronomy/Space Context Data
        astronomy_data = [
            {
                "category": "astronomy",
                "subcategory": "space_environment",
                "title": "Space Environment Challenges",
                "content": "Space presents unique challenges: microgravity affects body systems, radiation exposure, extreme temperatures, and the psychological impact of seeing Earth from space (overview effect).",
                "keywords": ["space", "microgravity", "radiation", "temperature", "environment", "earth", "overview"],
                "priority": 4
            },
            {
                "category": "astronomy",
                "subcategory": "mission_phases",
                "title": "Space Mission Phases",
                "content": "Space missions have distinct phases: pre-launch training, launch, orbital operations, and return. Each phase presents different psychological challenges and requires different support strategies.",
                "keywords": ["mission", "launch", "orbit", "return", "training", "phases", "operations"],
                "priority": 3
            },
            {
                "category": "astronomy",
                "subcategory": "communication_delays",
                "title": "Communication Delays in Deep Space",
                "content": "Deep space missions face significant communication delays with Earth (up to 20+ minutes each way). This requires astronauts to be more autonomous and self-reliant for psychological support.",
                "keywords": ["communication", "delay", "earth", "autonomous", "deep space", "contact"],
                "priority": 3
            },
            {
                "category": "astronomy",
                "subcategory": "life_support",
                "title": "Life Support Systems",
                "content": "Spacecraft life support systems provide oxygen, water, and waste management. Understanding these systems helps astronauts feel more secure and in control of their environment.",
                "keywords": ["life support", "oxygen", "water", "systems", "environmental", "control"],
                "priority": 2
            },
            {
                "category": "astronomy",
                "subcategory": "emergency_procedures",
                "title": "Emergency Response in Space",
                "content": "Space missions require extensive emergency training. Astronauts must remain calm and follow procedures during emergencies, which can be psychologically challenging.",
                "keywords": ["emergency", "procedures", "safety", "training", "crisis", "response"],
                "priority": 4
            }
        ]
        
        # Convert to ContextItem objects
        all_data = psychological_data + astronomy_data
        for item in all_data:
            context_item = ContextItem(
                category=item["category"],
                subcategory=item["subcategory"],
                title=item["title"],
                content=item["content"],
                keywords=item["keywords"],
                priority=item["priority"]
            )
            self.context_items.append(context_item)
    
    def search_context(self, query: str, max_results: int = 3) -> List[ContextItem]:
        """
        Search for relevant context based on query
        
        Args:
            query: The input query to match against
            max_results: Maximum number of context items to return
            
        Returns:
            List of relevant ContextItem objects sorted by relevance
        """
        query_lower = query.lower()
        scored_items = []
        
        for item in self.context_items:
            score = 0
            has_match = False
            
            # Check keyword matches
            for keyword in item.keywords:
                if keyword.lower() in query_lower:
                    score += 2  # Keyword match gets higher weight
                    has_match = True
            
            # Check title and content matches
            if item.title.lower() in query_lower:
                score += 3
                has_match = True
            if item.content.lower() in query_lower:
                score += 1
                has_match = True
            
            # Only add priority bonus if there's a match
            if has_match:
                score += item.priority * 0.5
                scored_items.append((score, item))
        
        # Sort by score (highest first) and return top results
        scored_items.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in scored_items[:max_results]]
    
    def get_context_for_prompt(self, query: str) -> str:
        """
        Get formatted context string for Gemini prompt
        
        Args:
            query: The input query
            
        Returns:
            Formatted context string to append to prompt
        """
        relevant_items = self.search_context(query)
        
        if not relevant_items:
            return "No specific context found for this query."
        
        context_parts = ["RELEVANT CONTEXT FOR ASTRONAUT SUPPORT:"]
        
        for item in relevant_items:
            context_parts.append(f"\n[{item.category.upper()}] {item.title}")
            context_parts.append(f"{item.content}")
        
        return "\n".join(context_parts)
    
    def add_context_item(self, category: str, subcategory: str, title: str, 
                        content: str, keywords: List[str], priority: int = 3):
        """Add a new context item to the database"""
        item = ContextItem(category, subcategory, title, content, keywords, priority)
        self.context_items.append(item)
    
    def get_all_context(self) -> List[ContextItem]:
        """Get all context items (for debugging/inspection)"""
        return self.context_items

# Example usage and testing
if __name__ == "__main__":
    db = ContextDatabase()
    
    # Test queries
    test_queries = [
        "I'm feeling stressed about the mission",
        "I can't sleep properly",
        "I feel isolated from my crew",
        "What should I do in an emergency?",
        "I'm worried about radiation exposure"
    ]
    
    print("Testing Context Database:")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 30)
        context = db.get_context_for_prompt(query)
        print(context)
        print()
