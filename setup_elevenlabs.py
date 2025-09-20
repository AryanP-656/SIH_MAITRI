"""
Setup script for ElevenLabs integration
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_elevenlabs():
    """Setup ElevenLabs API key"""
    print("\n🔑 ElevenLabs Setup")
    print("=" * 30)
    
    print("1. Go to https://elevenlabs.io/")
    print("2. Sign up for a free account")
    print("3. Go to your profile and copy your API key")
    print("4. Paste it below")
    
    api_key = input("\nEnter your ElevenLabs API key: ").strip()
    
    if api_key:
        # Set environment variable
        os.environ['ELEVENLABS_API_KEY'] = api_key
        
        # Set permanently for Windows
        try:
            subprocess.run([
                "powershell", "-Command", 
                f"[Environment]::SetEnvironmentVariable('ELEVENLABS_API_KEY', '{api_key}', 'User')"
            ], check=True)
            print("✅ ElevenLabs API key set permanently!")
        except:
            print("⚠️ Could not set permanent environment variable. Please set it manually:")
            print(f"$env:ELEVENLABS_API_KEY='{api_key}'")
        
        return True
    else:
        print("❌ No API key provided")
        return False

def test_elevenlabs():
    """Test ElevenLabs connection"""
    print("\n🧪 Testing ElevenLabs...")
    
    try:
        from elevenlabs import generate, play
        import os
        
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key:
            print("❌ ELEVENLABS_API_KEY not found")
            return False
        
        # Test with a simple phrase
        audio = generate(
            text="Hello, this is a test of ElevenLabs text to speech.",
            voice="EXAVITQu4vr4xnSDxMaL",  # Bella voice
            model="eleven_multilingual_v2"
        )
        
        print("✅ ElevenLabs connection successful!")
        print("🔊 Playing test audio...")
        play(audio)
        
        return True
        
    except Exception as e:
        print(f"❌ ElevenLabs test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 MAITRI ElevenLabs Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Setup ElevenLabs
    if setup_elevenlabs():
        # Test the setup
        if test_elevenlabs():
            print("\n🎉 Setup complete! You can now run:")
            print("python speech_maitri_elevenlabs.py")
        else:
            print("\n⚠️ Setup completed but ElevenLabs test failed.")
            print("You can still use the fallback TTS.")
    else:
        print("\n⚠️ ElevenLabs setup skipped. You can set it up later.")

if __name__ == "__main__":
    main()

