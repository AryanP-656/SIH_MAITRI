"""
Interactive MAITRI Test
Enter queries manually to test the system
"""

import os
from gemini_integration import MAITRIGeminiIntegration

def main():
    """Interactive testing interface"""
    
    print("🚀 MAITRI Interactive Test")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found. Please set your API key first.")
        print("Run: $env:GEMINI_API_KEY='your_api_key_here'")
        return
    
    try:
        # Initialize MAITRI
        print("🔧 Initializing MAITRI...")
        maitri = MAITRIGeminiIntegration(api_key)
        
        # Test connection
        if not maitri.test_connection():
            print("❌ Failed to connect to Gemini API")
            return
        
        print("✅ MAITRI ready!")
        print("\n" + "="*50)
        print("INTERACTIVE TESTING")
        print("="*50)
        print("Enter queries to test MAITRI (type 'quit' to exit)")
        print("You can also simulate face/voice data")
        print("\nExample queries:")
        print("- I'm feeling stressed")
        print("- I can't sleep")
        print("- I'm angry at my crewmate")
        print("- I'm hungry")
        print("- I feel isolated")
        print("-" * 50)
        
        while True:
            print("\n" + "="*30)
            
            # Get user input
            query = input("👨‍🚀 Astronaut Query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Safe travels!")
                break
            
            if not query:
                print("Please enter a query.")
                continue
            
            # Ask for sentiment data (optional)
            print("\n📊 Sentiment Data (optional - press Enter to skip):")
            face_emotion = input("Facial emotion (e.g., anxious, happy, tired): ").strip()
            voice_emotion = input("Voice emotion (e.g., stressed, calm, angry): ").strip()
            
            # Create sentiment data if provided
            sentiment_data = None
            if face_emotion or voice_emotion:
                sentiment_data = {
                    "facial_emotion": face_emotion or "neutral",
                    "voice_emotion": voice_emotion or "neutral",
                    "confidence": 0.85,
                    "timestamp": "2024-01-15T10:30:00Z"
                }
                print(f"📊 Using sentiment: Face={face_emotion}, Voice={voice_emotion}")
            
            # Get response
            print("\n🤖 MAITRI is thinking...")
            try:
                result = maitri.get_response(query, sentiment_data)
                
                if result['success']:
                    print(f"\n🤖 MAITRI Response:")
                    print("-" * 30)
                    print(result['response'])
                    print("-" * 30)
                    print(f"📚 Context used: {len(result['context_used'])} items")
                    
                    # Show context details
                    if result['context_used']:
                        print("\n📖 Context details:")
                        for i, item in enumerate(result['context_used'], 1):
                            print(f"  {i}. {item.category.upper()}: {item.title}")
                else:
                    print(f"❌ Error: {result['error']}")
                    
            except Exception as e:
                print(f"❌ Error getting response: {e}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def quick_test():
    """Quick test with predefined scenarios"""
    print("🚀 MAITRI Quick Test")
    print("=" * 30)
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found.")
        return
    
    try:
        maitri = MAITRIGeminiIntegration(api_key)
        
        # Quick test scenarios
        scenarios = [
            {
                "query": "I'm feeling really stressed",
                "sentiment": {"facial_emotion": "anxious", "voice_emotion": "stressed"}
            },
            {
                "query": "I can't sleep properly",
                "sentiment": {"facial_emotion": "tired", "voice_emotion": "exhausted"}
            },
            {
                "query": "I'm getting angry",
                "sentiment": {"facial_emotion": "angry", "voice_emotion": "frustrated"}
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n--- Test {i} ---")
            print(f"Query: {scenario['query']}")
            
            result = maitri.get_response(scenario['query'], scenario['sentiment'])
            
            if result['success']:
                print(f"Response: {result['response'][:200]}...")
                print(f"Context: {len(result['context_used'])} items")
            else:
                print(f"Error: {result['error']}")
            
            print("-" * 30)
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        main()

