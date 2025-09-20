"""
Simple ElevenLabs test
"""

import os
from elevenlabs import generate, play

def test_elevenlabs():
    """Test ElevenLabs with current API key"""
    
    # Get API key
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ ELEVENLABS_API_KEY not found")
        return False
    
    print(f"🔑 API Key found: {api_key[:10]}...")
    
    try:
        # Test with simple text
        print("🧪 Testing ElevenLabs...")
        audio = generate(
            text="Hello, this is a test of ElevenLabs text to speech.",
            voice="EXAVITQu4vr4xnSDxMaL",  # Bella voice
            model="eleven_multilingual_v2"
        )
        
        print("✅ ElevenLabs test successful!")
        print("🔊 Playing test audio...")
        play(audio)
        
        return True
        
    except Exception as e:
        print(f"❌ ElevenLabs test failed: {e}")
        return False

if __name__ == "__main__":
    test_elevenlabs()

