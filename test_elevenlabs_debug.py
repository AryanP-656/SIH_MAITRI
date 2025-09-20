"""
Debug ElevenLabs API key issue
"""

import os

def debug_elevenlabs():
    """Debug ElevenLabs API key"""
    
    print("🔍 Debugging ElevenLabs API Key...")
    print("=" * 40)
    
    # Check environment variable
    api_key = os.getenv('ELEVENLABS_API_KEY')
    print(f"Environment variable: {api_key}")
    
    if not api_key:
        print("❌ No API key found in environment")
        return
    
    # Check key format
    print(f"Key length: {len(api_key)}")
    print(f"Key starts with: {api_key[:10]}...")
    print(f"Key ends with: ...{api_key[-10:]}")
    
    # Check if it looks like a valid key
    if api_key.startswith('sk_'):
        print("✅ Key format looks correct (starts with 'sk_')")
    else:
        print("⚠️ Key format might be incorrect (should start with 'sk_')")
    
    # Try to set it explicitly
    print("\n🔄 Setting API key explicitly...")
    os.environ['ELEVENLABS_API_KEY'] = api_key
    
    # Test import
    try:
        from elevenlabs import generate, play
        print("✅ ElevenLabs import successful")
        
        # Test with explicit API key
        print("🧪 Testing with explicit API key...")
        audio = generate(
            text="Hello test",
            voice="EXAVITQu4vr4xnSDxMaL",
            model="eleven_multilingual_v2"
        )
        print("✅ Generate successful!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Try alternative approach
        print("\n🔄 Trying alternative approach...")
        try:
            from elevenlabs import set_api_key
            set_api_key(api_key)
            print("✅ API key set with set_api_key()")
            
            from elevenlabs import generate, play
            audio = generate(
                text="Hello test",
                voice="EXAVITQu4vr4xnSDxMaL",
                model="eleven_multilingual_v2"
            )
            print("✅ Generate successful with set_api_key()!")
            
        except Exception as e2:
            print(f"❌ Alternative approach failed: {e2}")

if __name__ == "__main__":
    debug_elevenlabs()

