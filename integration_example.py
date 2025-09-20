"""
MAITRI Integration Example
Shows how to integrate face/voice sentiment analysis with Gemini responses
"""

from gemini_integration import MAITRIGeminiIntegration
import os

def simulate_face_voice_analysis():
    """
    Simulate your existing face and voice analysis
    Replace this with your actual SigLIP2 and voice analysis code
    """
    # Simulate face analysis (SigLIP2)
    facial_emotion = "anxious"  # Your SigLIP2 result
    face_confidence = 0.87
    
    # Simulate voice analysis (Hugging Face)
    voice_emotion = "stressed"  # Your voice analysis result
    voice_confidence = 0.92
    
    # Combine into sentiment data
    sentiment_data = {
        "facial_emotion": facial_emotion,
        "voice_emotion": voice_emotion,
        "confidence": (face_confidence + voice_confidence) / 2,  # Average confidence
        "timestamp": "2024-01-15T10:30:00Z"
    }
    
    return sentiment_data

def main():
    """Main integration example"""
    
    # Check if API key is available
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found. Please set your API key first.")
        print("Run: $env:GEMINI_API_KEY='your_api_key_here'")
        return
    
    try:
        # Initialize MAITRI
        print("🚀 Initializing MAITRI with Gemini 2.0 Flash...")
        maitri = MAITRIGeminiIntegration(api_key)
        
        # Test connection
        if not maitri.test_connection():
            print("❌ Failed to connect to Gemini API")
            return
        
        print("✅ Connected to Gemini API successfully!")
        
        # Simulate different scenarios
        scenarios = [
            {
                "query": "I'm feeling really stressed about the mission",
                "face_emotion": "anxious",
                "voice_emotion": "stressed"
            },
            {
                "query": "I can't sleep properly in this environment", 
                "face_emotion": "tired",
                "voice_emotion": "exhausted"
            },
            {
                "query": "I'm getting angry at my crewmate",
                "face_emotion": "angry", 
                "voice_emotion": "frustrated"
            }
        ]
        
        print("\n" + "="*60)
        print("TESTING INTEGRATED RESPONSES")
        print("="*60)
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n--- Scenario {i} ---")
            print(f"Query: {scenario['query']}")
            print(f"Face: {scenario['face_emotion']}")
            print(f"Voice: {scenario['voice_emotion']}")
            
            # Create sentiment data
            sentiment_data = {
                "facial_emotion": scenario['face_emotion'],
                "voice_emotion": scenario['voice_emotion'],
                "confidence": 0.85,
                "timestamp": "2024-01-15T10:30:00Z"
            }
            
            # Get integrated response
            result = maitri.get_response(scenario['query'], sentiment_data)
            
            if result['success']:
                print(f"\nMAITRI Response:")
                print(f"{result['response']}")
                print(f"\nContext used: {len(result['context_used'])} items")
            else:
                print(f"Error: {result['error']}")
            
            print("-" * 50)
    
    except Exception as e:
        print(f"❌ Error: {e}")

def show_integration_code():
    """Show how to integrate with your existing code"""
    print("\n" + "="*60)
    print("INTEGRATION WITH YOUR EXISTING CODE")
    print("="*60)
    
    print("""
# In your existing sentiment analysis code:

# 1. After your SigLIP2 face analysis:
facial_emotion = "anxious"  # Your SigLIP2 result
face_confidence = 0.87

# 2. After your voice analysis:
voice_emotion = "stressed"  # Your voice analysis result  
voice_confidence = 0.92

# 3. Combine the data:
sentiment_data = {
    "facial_emotion": facial_emotion,
    "voice_emotion": voice_emotion,
    "confidence": (face_confidence + voice_confidence) / 2,
    "timestamp": "2024-01-15T10:30:00Z"
}

# 4. Get user input (from your UI/input system):
user_input = "I'm feeling overwhelmed"

# 5. Get MAITRI response:
from gemini_integration import MAITRIGeminiIntegration
maitri = MAITRIGeminiIntegration()  # Uses GEMINI_API_KEY env var
result = maitri.get_response(user_input, sentiment_data)

# 6. Display response:
print(result['response'])
""")

if __name__ == "__main__":
    # Show integration code
    show_integration_code()
    
    # Run the example
    main()
