"""
MAITRI Speech-to-Speech Interface
Real-time voice conversation with MAITRI
"""

import os
import time
import threading
import queue
from gemini_integration import MAITRIGeminiIntegration

# Speech-to-Text
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️ speech_recognition not installed. Install with: pip install SpeechRecognition")

# Text-to-Speech
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ pyttsx3 not installed. Install with: pip install pyttsx3")

class SpeechMAITRI:
    """Speech-to-speech interface for MAITRI"""
    
    def __init__(self, api_key=None):
        """Initialize speech interface"""
        self.maitri = MAITRIGeminiIntegration(api_key)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize TTS
        if TTS_AVAILABLE:
            self.tts_engine = pyttsx3.init()
            self._configure_tts()
        
        # Conversation state
        self.conversation_active = False
        self.audio_queue = queue.Queue()
        
        print("🎤 Speech MAITRI initialized!")
        print("💬 Say 'start conversation' to begin, 'stop' to end")
    
    def _configure_tts(self):
        """Configure text-to-speech settings"""
        if not TTS_AVAILABLE:
            return
            
        # Set voice properties
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Try to find a female voice (more suitable for MAITRI)
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        
        # Set speech rate and volume
        self.tts_engine.setProperty('rate', 180)  # Speed
        self.tts_engine.setProperty('volume', 0.9)  # Volume
    
    def speak(self, text):
        """Convert text to speech"""
        if not TTS_AVAILABLE:
            print(f"🔊 MAITRI: {text}")
            return
        
        print(f"🔊 MAITRI: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self, timeout=5):
        """Listen for speech input"""
        if not SPEECH_AVAILABLE:
            return input("👨‍🚀 Type your message: ")
        
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            print("🔄 Processing speech...")
            # Recognize speech
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
        # Simple keyword-based sentiment simulation
        # In real implementation, this would come from your SigLIP2 + voice analysis
        
        text_lower = text.lower()
        
        # Face emotion simulation
        if any(word in text_lower for word in ['stressed', 'anxious', 'worried', 'overwhelmed']):
            face_emotion = 'anxious'
        elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'frustrated']):
            face_emotion = 'angry'
        elif any(word in text_lower for word in ['tired', 'exhausted', 'sleepy']):
            face_emotion = 'tired'
        elif any(word in text_lower for word in ['happy', 'excited', 'great', 'wonderful']):
            face_emotion = 'happy'
        else:
            face_emotion = 'neutral'
        
        # Voice emotion simulation (similar logic)
        if any(word in text_lower for word in ['stressed', 'anxious', 'worried']):
            voice_emotion = 'stressed'
        elif any(word in text_lower for word in ['angry', 'mad', 'furious']):
            voice_emotion = 'angry'
        elif any(word in text_lower for word in ['tired', 'exhausted']):
            voice_emotion = 'exhausted'
        elif any(word in text_lower for word in ['happy', 'excited', 'great']):
            voice_emotion = 'happy'
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
        
        # Get MAITRI response
        result = self.maitri.get_response(text, sentiment_data)
        
        if result['success']:
            self.speak(result['response'])
        else:
            self.speak("I'm sorry, I'm having trouble processing that. Could you try again?")
    
    def start_conversation(self):
        """Start the speech conversation loop"""
        if not SPEECH_AVAILABLE or not TTS_AVAILABLE:
            print("❌ Speech features not available. Please install required packages:")
            print("pip install SpeechRecognition pyttsx3")
            return
        
        self.conversation_active = True
        self.speak("Hello! I'm MAITRI, your AI assistant. I'm here to support your psychological and physical well-being during this mission. How are you feeling today?")
        
        while self.conversation_active:
            try:
                # Listen for user input
                user_input = self.listen(timeout=10)
                
                if user_input:
                    # Check for stop commands
                    if any(word in user_input.lower() for word in ['stop', 'end', 'quit', 'goodbye']):
                        self.speak("Thank you for talking with me. Stay safe and take care!")
                        self.conversation_active = False
                        break
                    
                    # Process the conversation
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
        print("=" * 40)
        
        scenarios = [
            "I'm feeling really stressed about the mission",
            "I can't sleep properly in this environment",
            "I'm getting angry at my crewmate",
            "I'm hungry and need something to eat"
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n--- Demo Scenario {i} ---")
            print(f"Simulating: '{scenario}'")
            
            # Simulate sentiment
            sentiment_data = self.simulate_sentiment_analysis(scenario)
            print(f"Detected: Face={sentiment_data['facial_emotion']}, Voice={sentiment_data['voice_emotion']}")
            
            # Get response
            result = self.maitri.get_response(scenario, sentiment_data)
            
            if result['success']:
                self.speak(result['response'])
            else:
                print(f"Error: {result['error']}")
            
            input("\nPress Enter for next scenario...")

def main():
    """Main function"""
    print("🚀 MAITRI Speech Interface")
    print("=" * 40)
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found. Please set your API key first.")
        return
    
    try:
        # Initialize speech MAITRI
        speech_maitri = SpeechMAITRI(api_key)
        
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

