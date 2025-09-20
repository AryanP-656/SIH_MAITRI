# MAITRI - Cross-Platform Setup Guide

## 🚀 MAITRI: AI Assistant for Astronaut Well-being

MAITRI is a multimodal AI assistant designed to provide psychological and physical well-being support for astronauts during space missions. It features speech-to-speech conversation, context-aware responses, and sentiment analysis integration.

## 🌍 Platform Support

- ✅ **Windows** (PowerShell/CMD)
- ✅ **Ubuntu/Linux** (Bash)
- ✅ **macOS** (Terminal)
- ✅ **Cross-platform** Python

## 📋 Quick Start

### Prerequisites

- Python 3.8+
- Internet connection
- Microphone (for speech features)
- Speakers/Headphones

### 1. Clone/Download Project

```bash
git clone <repository-url>
cd SIH_MAITRI
```

### 2. Platform-Specific Setup

#### Windows

```powershell
# Run setup script
.\setup_windows.ps1

# Or manually
pip install -r requirements.txt
winget install ffmpeg
```

#### Ubuntu/Linux

```bash
# Make setup script executable
chmod +x setup_ubuntu.sh

# Run setup script
./setup_ubuntu.sh

# Or follow UBUNTU_SETUP.md for manual setup
```

#### macOS

```bash
# Install dependencies
brew install ffmpeg portaudio
pip install -r requirements.txt
```

### 3. Set API Keys

#### Windows (PowerShell)

```powershell
$env:GEMINI_API_KEY="your_gemini_key"
$env:ELEVENLABS_API_KEY="your_elevenlabs_key"
```

#### Linux/macOS (Bash)

```bash
export GEMINI_API_KEY="your_gemini_key"
export ELEVENLABS_API_KEY="your_elevenlabs_key"
```

### 4. Test the System

```bash
# Test basic functionality
python demo.py

# Test speech interface
python speech_maitri_no_ffmpeg.py
```

## 🎯 Core Features

### 1. Context Database

- **Psychological support** information
- **Astronomy/space** knowledge
- **Automatic context retrieval** based on queries
- **Extensible** - add custom context

### 2. Speech-to-Speech Interface

- **Real-time speech recognition**
- **Text-to-speech** with ElevenLabs
- **Fallback TTS** (pyttsx3) if needed
- **Cross-platform** audio support

### 3. Gemini Integration

- **Context-aware responses**
- **Sentiment analysis** integration
- **Automatic model selection**
- **Error handling** and fallbacks

### 4. Sentiment Analysis

- **Simulated face/voice** emotion detection
- **Ready for integration** with real analysis
- **Configurable** emotion mapping

## 📁 File Structure

```
SIH_MAITRI/
├── context_database.py          # Knowledge base
├── gemini_integration.py        # Gemini API integration
├── speech_maitri_no_ffmpeg.py   # Speech interface (recommended)
├── speech_maitri_fixed.py       # Speech interface (with FFmpeg)
├── interactive_test.py          # Text interface
├── demo.py                      # Demo scenarios
├── requirements.txt             # Python dependencies
├── setup_windows.ps1            # Windows setup
├── setup_ubuntu.sh              # Ubuntu setup
├── UBUNTU_SETUP.md             # Ubuntu guide
└── README_CROSS_PLATFORM.md    # This guide
```

## 🔧 Usage Examples

### Basic Text Interface

```python
from gemini_integration import MAITRIGeminiIntegration

# Initialize
maitri = MAITRIGeminiIntegration()

# Get response
result = maitri.get_response("I'm feeling stressed", {
    "facial_emotion": "anxious",
    "voice_emotion": "stressed"
})

print(result['response'])
```

### Speech Interface

```python
from speech_maitri_no_ffmpeg import SpeechMAITRINoFFmpeg

# Initialize
speech_maitri = SpeechMAITRINoFFmpeg()

# Start conversation
speech_maitri.start_conversation()
```

### Custom Context

```python
from context_database import ContextDatabase

db = ContextDatabase()
db.add_custom_context(
    category="psychological",
    subcategory="custom_topic",
    title="Custom Title",
    content="Your content here",
    keywords=["keyword1", "keyword2"],
    priority=3
)
```

## 🎬 Demo Scenarios

The system includes predefined scenarios for testing:

1. **Stress Management**: "I'm feeling really stressed about the mission"
2. **Sleep Issues**: "I can't sleep properly in this environment"
3. **Team Dynamics**: "I'm getting angry at my crewmate"
4. **Nutrition**: "I'm hungry and need something to eat"
5. **Isolation**: "I feel isolated and lonely"
6. **Excitement**: "I'm excited about the spacewalk tomorrow"

## 🔑 API Keys Required

### 1. Gemini API Key

- **Source**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Cost**: Free tier available
- **Usage**: Text generation and responses

### 2. ElevenLabs API Key

- **Source**: [ElevenLabs](https://elevenlabs.io/)
- **Cost**: Free tier available
- **Usage**: Text-to-speech conversion

## 🐛 Troubleshooting

### Common Issues

#### 1. FFmpeg Not Found

- **Windows**: `winget install ffmpeg`
- **Ubuntu**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`

#### 2. PyAudio Installation Failed

- **Windows**: Usually works with pip
- **Ubuntu**: `sudo apt install portaudio19-dev python3-dev`
- **macOS**: `brew install portaudio`

#### 3. Microphone Not Working

- Check system audio permissions
- Test with system audio tools
- Verify microphone is not muted

#### 4. API Key Issues

- Verify keys are set correctly
- Check key validity and permissions
- Test individual components

### Platform-Specific Issues

#### Windows

- Use PowerShell instead of CMD
- Check Windows Defender settings
- Verify Python path in environment

#### Ubuntu/Linux

- Check audio group membership
- Verify ALSA/PulseAudio setup
- Test with system audio tools

#### macOS

- Check microphone permissions
- Verify Homebrew installation
- Test with system audio tools

## 🚀 Integration with Existing Code

### Sentiment Analysis Integration

```python
# Your existing sentiment analysis
facial_emotion = "anxious"  # From SigLIP2
voice_emotion = "stressed"  # From voice analysis

# MAITRI integration
sentiment_data = {
    "facial_emotion": facial_emotion,
    "voice_emotion": voice_emotion,
    "confidence": 0.85,
    "timestamp": "2024-01-15T10:30:00Z"
}

result = maitri.get_response(user_input, sentiment_data)
```

### Custom Voice Integration

```python
# Change voice in speech_maitri_no_ffmpeg.py
self.voice_id = "EXAVITQu4vr4xnSDxMaL"  # Change to different voice ID
```

## 📊 Performance Tips

1. **Use virtual environments** to avoid conflicts
2. **Test with demo mode** before live conversation
3. **Check audio permissions** if speech recognition fails
4. **Use fallback TTS** if ElevenLabs has issues
5. **Monitor API usage** to avoid rate limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple platforms
5. Submit a pull request

## 📄 License

This project is for educational/hackathon purposes.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Test individual components
4. Check API key validity
5. Review platform-specific guides

## 🎯 Next Steps

1. **Test basic functionality** with demo mode
2. **Try speech interface** with predefined scenarios
3. **Integrate with your sentiment analysis** code
4. **Customize context database** for your needs
5. **Prepare for demo** with realistic scenarios

---

**Happy coding! 🚀✨**
