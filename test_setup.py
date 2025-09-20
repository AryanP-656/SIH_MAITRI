"""
MAITRI Setup Test Script
Tests all components to ensure proper installation
"""

import os
import sys

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def test_imports():
    """Test required imports"""
    print("\n📚 Testing Python imports...")
    
    imports = [
        ("google.generativeai", "Google Generative AI"),
        ("speech_recognition", "Speech Recognition"),
        ("pyttsx3", "PyTTSx3"),
        ("elevenlabs", "ElevenLabs"),
        ("requests", "Requests")
    ]
    
    all_ok = True
    for module, name in imports:
        try:
            __import__(module)
            print(f"✅ {name} - OK")
        except ImportError as e:
            print(f"❌ {name} - Missing: {e}")
            all_ok = False
    
    return all_ok

def test_api_keys():
    """Test API keys"""
    print("\n🔑 Testing API keys...")
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
    
    gemini_ok = bool(gemini_key)
    elevenlabs_ok = bool(elevenlabs_key)
    
    if gemini_ok:
        print(f"✅ Gemini API Key - OK ({gemini_key[:10]}...)")
    else:
        print("❌ Gemini API Key - Missing")
    
    if elevenlabs_ok:
        print(f"✅ ElevenLabs API Key - OK ({elevenlabs_key[:10]}...)")
    else:
        print("❌ ElevenLabs API Key - Missing")
    
    return gemini_ok and elevenlabs_ok

def test_ffmpeg():
    """Test FFmpeg installation"""
    print("\n🎵 Testing FFmpeg...")
    
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg - OK")
            return True
        else:
            print("❌ FFmpeg - Not working")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ FFmpeg - Not found")
        return False

def test_audio_system():
    """Test audio system"""
    print("\n🎤 Testing audio system...")
    
    try:
        import speech_recognition as sr
        import pyttsx3
        
        # Test microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("✅ Microphone - Available")
        
        # Test TTS
        engine = pyttsx3.init()
        print("✅ Text-to-Speech - Available")
        
        return True
    except Exception as e:
        print(f"❌ Audio system - Error: {e}")
        return False

def test_maitri_components():
    """Test MAITRI components"""
    print("\n🤖 Testing MAITRI components...")
    
    try:
        from context_database import ContextDatabase
        from gemini_integration import MAITRIGeminiIntegration
        
        # Test context database
        db = ContextDatabase()
        context = db.get_context_for_prompt("I'm feeling stressed")
        if context and "RELEVANT CONTEXT" in context:
            print("✅ Context Database - OK")
        else:
            print("❌ Context Database - Not working")
            return False
        
        # Test Gemini integration (if API key available)
        if os.getenv('GEMINI_API_KEY'):
            try:
                maitri = MAITRIGeminiIntegration()
                if maitri.test_connection():
                    print("✅ Gemini Integration - OK")
                else:
                    print("❌ Gemini Integration - Connection failed")
                    return False
            except Exception as e:
                print(f"❌ Gemini Integration - Error: {e}")
                return False
        else:
            print("⚠️ Gemini Integration - Skipped (no API key)")
        
        return True
    except Exception as e:
        print(f"❌ MAITRI components - Error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 MAITRI Setup Test")
    print("=" * 40)
    
    tests = [
        ("Python Version", test_python_version),
        ("Python Imports", test_imports),
        ("API Keys", test_api_keys),
        ("FFmpeg", test_ffmpeg),
        ("Audio System", test_audio_system),
        ("MAITRI Components", test_maitri_components)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} - Error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! MAITRI is ready to use.")
        print("\nNext steps:")
        print("1. Run: python demo.py")
        print("2. Run: python speech_maitri_no_ffmpeg.py")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please check the issues above.")
        print("\nCommon fixes:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Set API keys: export GEMINI_API_KEY='your_key'")
        print("- Install FFmpeg: sudo apt install ffmpeg (Ubuntu)")

if __name__ == "__main__":
    main()
