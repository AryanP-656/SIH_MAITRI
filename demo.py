"""
MAITRI Demo Script
Demonstrates the context database and Gemini integration
"""

import os
from gemini_integration import MAITRIGeminiIntegration
from context_database import ContextDatabase

def demo_context_database():
    """Demo the context database functionality"""
    print("🔍 DEMO: Context Database")
    print("=" * 50)
    
    db = ContextDatabase()
    
    # Test queries
    test_queries = [
        "I'm feeling stressed about the mission",
        "I can't sleep properly",
        "I feel isolated from my crew",
        "What should I do in an emergency?",
        "I'm worried about radiation exposure"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 30)
        context = db.get_context_for_prompt(query)
        print(context)
        print()

def demo_gemini_integration():
    """Demo the Gemini integration (requires API key)"""
    print("\n🤖 DEMO: Gemini Integration")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("To test Gemini integration, set your API key:")
        print("export GEMINI_API_KEY='your_api_key_here'")
        return
    
    try:
        # Initialize MAITRI
        maitri = MAITRIGeminiIntegration(api_key)
        
        # Test connection
        if not maitri.test_connection():
            print("❌ Failed to connect to Gemini API")
            return
        
        print("✅ Connected to Gemini API successfully!")
        
        # Demo queries
        demo_queries = [
            {
                "input": "I'm feeling really stressed about the upcoming spacewalk",
                "sentiment": {
                    "facial_emotion": "anxious",
                    "voice_emotion": "stressed",
                    "confidence": 0.85
                }
            },
            {
                "input": "I can't sleep properly in this environment",
                "sentiment": {
                    "facial_emotion": "tired",
                    "voice_emotion": "exhausted",
                    "confidence": 0.92
                }
            }
        ]
        
        for i, demo in enumerate(demo_queries, 1):
            print(f"\n--- Demo Query {i} ---")
            print(f"Input: {demo['input']}")
            print(f"Sentiment: {demo['sentiment']}")
            
            # Get response
            result = maitri.get_response(demo['input'], demo['sentiment'])
            
            if result['success']:
                print(f"MAITRI Response: {result['response']}")
                print(f"Context items used: {len(result['context_used'])}")
            else:
                print(f"Error: {result['error']}")
            
            print("-" * 40)
    
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_context_retrieval():
    """Demo just the context retrieval without Gemini"""
    print("\n📚 DEMO: Context Retrieval Only")
    print("=" * 50)
    
    db = ContextDatabase()
    
    # Show all available context categories
    all_items = db.get_all_context()
    categories = {}
    for item in all_items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item.subcategory)
    
    print("Available context categories:")
    for category, subcategories in categories.items():
        print(f"  {category}: {', '.join(set(subcategories))}")
    
    # Interactive context search
    print("\nEnter queries to test context retrieval (type 'quit' to exit):")
    while True:
        query = input("\nQuery: ").strip()
        if query.lower() == 'quit':
            break
        
        if query:
            context = db.get_context_for_prompt(query)
            print(f"\nContext for '{query}':")
            print("-" * 30)
            print(context)

if __name__ == "__main__":
    print("🚀 MAITRI DEMO")
    print("=" * 50)
    
    # Run context database demo
    demo_context_database()
    
    # Run Gemini integration demo (if API key available)
    demo_gemini_integration()
    
    # Interactive context retrieval demo
    demo_context_retrieval()
    
    print("\n✅ Demo completed!")

