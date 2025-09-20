"""
MAITRI Speech-to-Speech Interface (No FFmpeg Required)
Uses pyttsx3 as fallback when FFmpeg is not available
"""

import os
import time
import threading
import queue
import tempfile
from gemini_integration import MAITRIGeminiIntegration

# Speech-to-Text
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️ speech_recognition not installed. Install with: pip install SpeechRecognition")

# ElevenLabs TTS
try:
    from elevenlabs import generate, play, save, Voice, VoiceSettings, set_api_key
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    print("⚠️ elevenlabs not installed. Install with: pip install elevenlabs==0.2.26")

# Fallback TTS
try:
    import pyttsx3
    FALLBACK_TTS_AVAILABLE = True
except ImportError:
    FALLBACK_TTS_AVAILABLE = False

class SpeechMAITRINoFFmpeg:
    """Speech-to-speech interface for MAITRI with FFmpeg fallback"""
    
    def __init__(self, api_key=None, elevenlabs_api_key=None):
        """Initialize speech interface"""
        self.maitri = MAITRIGeminiIntegration(api_key)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # ElevenLabs configuration
        self.elevenlabs_api_key = elevenlabs_api_key or os.getenv('ELEVENLABS_API_KEY')
        self.voice_id = "EXAVITQu4vr4xnSDxMaL"  # Bella voice
        
        # Initialize TTS
        if FALLBACK_TTS_AVAILABLE:
            self.tts_engine = pyttsx3.init()
            self._configure_tts()
        
        # Conversation state
        self.conversation_active = False
        
        print("🎤 Speech MAITRI initialized!")
        print("💬 Say 'start conversation' to begin, 'stop' to end")
        
        if ELEVENLABS_AVAILABLE and self.elevenlabs_api_key:
            print("✅ ElevenLabs TTS ready!")
        elif FALLBACK_TTS_AVAILABLE:
            print("⚠️ Using fallback TTS (pyttsx3)")
        else:
            print("❌ No TTS available")
    
    def _configure_tts(self):
        """Configure TTS settings"""
        if not FALLBACK_TTS_AVAILABLE:
            return
            
        voices = self.tts_engine.getProperty('voices')
        if voices:
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.9)
    
    def speak_elevenlabs(self, text):
        """Convert text to speech using ElevenLabs"""
        if not ELEVENLABS_AVAILABLE or not self.elevenlabs_api_key:
            self.speak_fallback(text)
            return
        
        try:
            print(f"🔊 MAITRI: {text}")
            
            # Set API key
            set_api_key(self.elevenlabs_api_key)
            
            # Generate audio
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=self.voice_id,
                    settings=VoiceSettings(
                        stability=0.5,
                        similarity_boost=0.8,
                        style=0.2,
                        use_speaker_boost=True
                    )
                ),
                model="eleven_multilingual_v2"
            )
            
            # Try to play audio
            try:
                play(audio)
            except Exception as e:
                print(f"⚠️ Cannot play audio (FFmpeg issue): {e}")
                print("🔄 Using fallback TTS...")
                self.speak_fallback(text)
            
        except Exception as e:
            print(f"❌ ElevenLabs error: {e}")
            print("🔄 Falling back to pyttsx3...")
            self.speak_fallback(text)
    
    def speak_fallback(self, text):
        """Convert text to speech using fallback TTS"""
        if not FALLBACK_TTS_AVAILABLE:
            print(f"🔊 MAITRI: {text}")
            return
        
        print(f"🔊 MAITRI: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def speak(self, text):
        """Convert text to speech (uses best available method)"""
        if ELEVENLABS_AVAILABLE and self.elevenlabs_api_key:
            self.speak_elevenlabs(text)
        else:
            self.speak_fallback(text)
    
    def listen(self, timeout=5):
        """Listen for speech input"""
        if not SPEECH_AVAILABLE:
            return input("👨‍🚀 Type your message: ")
        
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            print("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"👨‍🚀 You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand speech")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
    
    def simulate_sentiment_analysis(self, text):
        """Simulate face/voice sentiment analysis based on text content"""
        text_lower = text.lower()
        
        # Enhanced sentiment detection
        if any(word in text_lower for word in ['stressed', 'anxious', 'worried', 'overwhelmed', 'pressure']):
            face_emotion = 'anxious'
        elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'frustrated', 'irritated']):
            face_emotion = 'angry'
        elif any(word in text_lower for word in ['tired', 'exhausted', 'sleepy', 'fatigue']):
            face_emotion = 'tired'
        elif any(word in text_lower for word in ['happy', 'excited', 'great', 'wonderful', 'amazing']):
            face_emotion = 'happy'
        elif any(word in text_lower for word in ['sad', 'down', 'depressed', 'lonely']):
            face_emotion = 'sad'
        else:
            face_emotion = 'neutral'
        
        # Voice emotion simulation
        if any(word in text_lower for word in ['stressed', 'anxious', 'worried', 'pressure']):
            voice_emotion = 'stressed'
        elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'frustrated']):
            voice_emotion = 'angry'
        elif any(word in text_lower for word in ['tired', 'exhausted', 'fatigue']):
            voice_emotion = 'exhausted'
        elif any(word in text_lower for word in ['happy', 'excited', 'great', 'wonderful']):
            voice_emotion = 'happy'
        elif any(word in text_lower for word in ['sad', 'down', 'depressed', 'lonely']):
            voice_emotion = 'sad'
        else:
            voice_emotion = 'calm'
        
        return {
            "facial_emotion": face_emotion,
            "voice_emotion": voice_emotion,
            "confidence": 0.85,
            "timestamp": "2024-01-15T10:30:00Z"
        }
    
    def process_conversation(self, text):
        """Process user input and generate response"""
        if not text:
            return
        
        # Simulate sentiment analysis
        sentiment_data = self.simulate_sentiment_analysis(text)
        print(f"📊 Detected: Face={sentiment_data['facial_emotion']}, Voice={sentiment_data['voice_emotion']}")
        
        # Get MAITRI response
        result = self.maitri.get_response(text, sentiment_data)
        
        if result['success']:
            self.speak(result['response'])
        else:
            self.speak("I'm sorry, I'm having trouble processing that. Could you try again?")
    
    def start_conversation(self):
        """Start the speech conversation loop"""
        if not SPEECH_AVAILABLE:
            print("❌ Speech recognition not available. Please install required packages:")
            print("pip install SpeechRecognition pyaudio")
            return
        
        if not ELEVENLABS_AVAILABLE and not FALLBACK_TTS_AVAILABLE:
            print("❌ No TTS available. Please install pyttsx3 or elevenlabs")
            return
        
        self.conversation_active = True
        self.speak("Hello! I'm MAITRI, your AI assistant. I'm here to support your psychological and physical well-being during this mission. How are you feeling today?")
        
        while self.conversation_active:
            try:
                user_input = self.listen(timeout=10)
                
                if user_input:
                    if any(word in user_input.lower() for word in ['stop', 'end', 'quit', 'goodbye']):
                        self.speak("Thank you for talking with me. Stay safe and take care!")
                        self.conversation_active = False
                        break
                    
                    self.process_conversation(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Conversation ended by user")
                self.conversation_active = False
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                self.speak("I encountered an error. Let's try again.")
    
    def demo_mode(self):
        """Demo mode with predefined scenarios"""
        print("🎬 MAITRI Speech Demo Mode")
        print("=" * 50)
        
        scenarios = [
            "I'm feeling really stressed about the mission",
            "I can't sleep properly in this environment", 
            "I'm getting angry at my crewmate",
            "I'm hungry and need something to eat",
            "I feel isolated and lonely",
            "I'm excited about the spacewalk tomorrow"
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n--- Demo Scenario {i} ---")
            print(f"Simulating: '{scenario}'")
            
            sentiment_data = self.simulate_sentiment_analysis(scenario)
            print(f"Detected: Face={sentiment_data['facial_emotion']}, Voice={sentiment_data['voice_emotion']}")
            
            result = self.maitri.get_response(scenario, sentiment_data)
            
            if result['success']:
                self.speak(result['response'])
            else:
                print(f"Error: {result['error']}")
            
            input("\nPress Enter for next scenario...")

def main():
    """Main function"""
    print("🚀 MAITRI Speech Interface (FFmpeg Fallback)")
    print("=" * 50)
    
    # Check API keys
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not gemini_api_key:
        print("❌ GEMINI_API_KEY not found. Please set your API key first.")
        return
    
    if not elevenlabs_api_key:
        print("⚠️ ELEVENLABS_API_KEY not found. Will use fallback TTS.")
        print("Get your key from: https://elevenlabs.io/")
    
    try:
        speech_maitri = SpeechMAITRINoFFmpeg(gemini_api_key, elevenlabs_api_key)
        
        print("\nChoose mode:")
        print("1. Live conversation (speech-to-speech)")
        print("2. Demo mode (predefined scenarios)")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            speech_maitri.start_conversation()
        elif choice == "2":
            speech_maitri.demo_mode()
        elif choice == "3":
            print("👋 Goodbye!")
        else:
            print("Invalid choice")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

