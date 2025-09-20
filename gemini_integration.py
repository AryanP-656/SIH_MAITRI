"""
Gemini API Integration for MAITRI
Handles context retrieval and prompt construction for Gemini API calls
"""

import os
import json
from typing import Dict, Any, Optional
import google.generativeai as genai
from context_database import ContextDatabase

class MAITRIGeminiIntegration:
    """Handles Gemini API integration with automatic context retrieval"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = 'gemini-2.0-flash-exp'):
        """
        Initialize the Gemini integration
        
        Args:
            api_key: Gemini API key. If None, will try to get from environment variable
            model_name: Gemini model to use (default: gemini-2.0-flash-exp)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not provided. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Try to initialize the model, fallback to alternatives if needed
        self.model = self._initialize_model(model_name)
        
        # Initialize context database
        self.context_db = ContextDatabase()
        
        # System prompt for MAITRI
        self.system_prompt = """You are MAITRI, an AI assistant designed to support astronauts' psychological and physical well-being during space missions. 

Your role:
- Provide empathetic, supportive responses to astronauts
- Offer practical coping strategies and psychological support
- Share relevant information about space environment and mission context
- Maintain a professional yet warm tone
- Focus on mental health, stress management, and mission success
- Never provide medical advice beyond general wellness guidance

You have access to a database of psychological and astronomy information that will be provided as context for each conversation."""
    
    def _initialize_model(self, preferred_model: str):
        """Initialize Gemini model with fallback options"""
        fallback_models = [
            preferred_model,
            'gemini-1.5-flash',
            'gemini-1.5-pro', 
            'gemini-pro'
        ]
        
        for model_name in fallback_models:
            try:
                model = genai.GenerativeModel(model_name)
                # Test the model with a simple query
                test_response = model.generate_content("Hello")
                print(f"✅ Using Gemini model: {model_name}")
                return model
            except Exception as e:
                print(f"❌ {model_name} failed: {str(e)[:100]}...")
                continue
        
        raise Exception("No working Gemini model found. Please check your API key and model availability.")
    
    def construct_prompt(self, user_input: str, sentiment_data: Optional[Dict] = None) -> str:
        """
        Construct a complete prompt for Gemini with context
        
        Args:
            user_input: The astronaut's input/query
            sentiment_data: Optional sentiment analysis data from face/voice
            
        Returns:
            Complete formatted prompt for Gemini
        """
        # Get relevant context
        context = self.context_db.get_context_for_prompt(user_input)
        
        # Build the prompt
        prompt_parts = [self.system_prompt]
        
        # Add context if available
        if context and context != "No specific context found for this query.":
            prompt_parts.append(f"\n{context}")
        
        # Add sentiment data if provided
        if sentiment_data:
            sentiment_info = self._format_sentiment_data(sentiment_data)
            prompt_parts.append(f"\nCURRENT SENTIMENT ANALYSIS:\n{sentiment_info}")
        
        # Add user input
        prompt_parts.append(f"\nASTRONAUT INPUT: {user_input}")
        
        # Add response instruction
        prompt_parts.append("\nPlease provide a supportive, helpful response as MAITRI:")
        
        return "\n".join(prompt_parts)
    
    def _format_sentiment_data(self, sentiment_data: Dict) -> str:
        """Format sentiment data for inclusion in prompt"""
        formatted = []
        
        if 'facial_emotion' in sentiment_data:
            formatted.append(f"Facial Emotion: {sentiment_data['facial_emotion']}")
        
        if 'voice_emotion' in sentiment_data:
            formatted.append(f"Voice Emotion: {sentiment_data['voice_emotion']}")
        
        if 'confidence' in sentiment_data:
            formatted.append(f"Confidence: {sentiment_data['confidence']:.2f}")
        
        if 'timestamp' in sentiment_data:
            formatted.append(f"Timestamp: {sentiment_data['timestamp']}")
        
        return "\n".join(formatted)
    
    def get_response(self, user_input: str, sentiment_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get a response from Gemini with automatic context retrieval
        
        Args:
            user_input: The astronaut's input/query
            sentiment_data: Optional sentiment analysis data
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Construct prompt with context
            prompt = self.construct_prompt(user_input, sentiment_data)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "response": response.text,
                "user_input": user_input,
                "context_used": self.context_db.search_context(user_input),
                "sentiment_data": sentiment_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "user_input": user_input,
                "sentiment_data": sentiment_data
            }
    
    def get_context_only(self, user_input: str) -> str:
        """
        Get only the context for a query (useful for debugging)
        
        Args:
            user_input: The input query
            
        Returns:
            Formatted context string
        """
        return self.context_db.get_context_for_prompt(user_input)
    
    def add_custom_context(self, category: str, subcategory: str, title: str, 
                          content: str, keywords: list, priority: int = 3):
        """Add custom context to the database"""
        self.context_db.add_context_item(category, subcategory, title, content, keywords, priority)
    
    def test_connection(self) -> bool:
        """Test if Gemini API connection is working"""
        try:
            test_response = self.model.generate_content("Hello, this is a test.")
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Note: You'll need to set your Gemini API key
    # export GEMINI_API_KEY="your_api_key_here"
    
    try:
        # Initialize (will use GEMINI_API_KEY environment variable)
        maitri = MAITRIGeminiIntegration()
        
        # Test connection
        if maitri.test_connection():
            print("✅ Gemini API connection successful!")
        else:
            print("❌ Gemini API connection failed!")
            exit(1)
        
        # Test queries
        test_cases = [
            {
                "input": "I'm feeling really stressed about the upcoming spacewalk",
                "sentiment": {
                    "facial_emotion": "anxious",
                    "voice_emotion": "stressed",
                    "confidence": 0.85,
                    "timestamp": "2024-01-15T10:30:00Z"
                }
            },
            {
                "input": "I can't sleep properly in this environment",
                "sentiment": {
                    "facial_emotion": "tired",
                    "voice_emotion": "exhausted",
                    "confidence": 0.92,
                    "timestamp": "2024-01-15T22:15:00Z"
                }
            },
            {
                "input": "What should I do if there's an emergency?",
                "sentiment": {
                    "facial_emotion": "concerned",
                    "voice_emotion": "worried",
                    "confidence": 0.78,
                    "timestamp": "2024-01-15T14:45:00Z"
                }
            }
        ]
        
        print("\n" + "="*60)
        print("TESTING MAITRI GEMINI INTEGRATION")
        print("="*60)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test Case {i} ---")
            print(f"Input: {test_case['input']}")
            print(f"Sentiment: {test_case['sentiment']}")
            
            # Get response
            result = maitri.get_response(test_case['input'], test_case['sentiment'])
            
            if result['success']:
                print(f"Response: {result['response']}")
                print(f"Context used: {len(result['context_used'])} items")
            else:
                print(f"Error: {result['error']}")
            
            print("-" * 40)
    
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please set your Gemini API key:")
        print("export GEMINI_API_KEY='your_api_key_here'")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
