"""
Test Gemini 2.0 Flash model
"""

import os
import google.generativeai as genai

def test_gemini_models():
    """Test different Gemini models"""
    
    # Check if API key is set
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found. Please set your API key first.")
        print("Run: $env:GEMINI_API_KEY='your_api_key_here'")
        return
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test different model names
        models_to_test = [
            'gemini-2.0-flash-exp',
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro'
        ]
        
        print("🧪 Testing Gemini models...")
        print("=" * 40)
        
        for model_name in models_to_test:
            try:
                print(f"\nTesting {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello, this is a test.")
                print(f"✅ {model_name}: Working!")
                print(f"Response: {response.text[:100]}...")
                break  # Use the first working model
                
            except Exception as e:
                print(f"❌ {model_name}: Failed - {str(e)[:100]}...")
                continue
        
        print(f"\n🎉 Using working model: {model_name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_gemini_models()

