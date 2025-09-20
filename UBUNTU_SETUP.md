# MAITRI Ubuntu Setup Guide

## Overview

This guide helps you set up MAITRI (AI Assistant for Astronaut Well-being) on Ubuntu Linux. MAITRI provides speech-to-speech conversation with context-aware psychological support for space missions.

## Prerequisites

- Ubuntu 20.04+ (or similar Linux distribution)
- Python 3.8+
- Internet connection for API keys

## Quick Setup

### 1. Clone/Download the Project

```bash
# If using git
git clone <repository-url>
cd SIH_MAITRI

# Or download and extract the project files
```

### 2. Install System Dependencies

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install FFmpeg (required for ElevenLabs audio)
sudo apt install ffmpeg

# Install audio dependencies
sudo apt install portaudio19-dev python3-pyaudio

# Install other dependencies
sudo apt install espeak espeak-data
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv maitri_env

# Activate virtual environment
source maitri_env/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 4. Install Python Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# If you get errors with pyaudio, try:
sudo apt install python3-dev
pip install pyaudio
```

### 5. Set Up API Keys

```bash
# Set Gemini API key
export GEMINI_API_KEY="your_gemini_api_key_here"

# Set ElevenLabs API key
export ELEVENLABS_API_KEY="your_elevenlabs_api_key_here"

# Make them permanent (add to ~/.bashrc)
echo 'export GEMINI_API_KEY="your_gemini_api_key_here"' >> ~/.bashrc
echo 'export ELEVENLABS_API_KEY="your_elevenlabs_api_key_here"' >> ~/.bashrc

# Reload bashrc
source ~/.bashrc
```

## Usage

### 1. Basic Text Interface

```bash
# Activate virtual environment
source maitri_env/bin/activate

# Run interactive text interface
python interactive_test.py
```

### 2. Speech-to-Speech Interface

```bash
# Run speech interface (with FFmpeg fallback)
python speech_maitri_no_ffmpeg.py

# Or run the fixed version (if FFmpeg is working)
python speech_maitri_fixed.py
```

### 3. Demo Mode

```bash
# Run demo with predefined scenarios
python demo.py
```

## Troubleshooting

### Common Issues

#### 1. FFmpeg Not Found

```bash
# Install FFmpeg
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

#### 2. PyAudio Installation Failed

```bash
# Install system dependencies first
sudo apt install portaudio19-dev python3-dev

# Then install PyAudio
pip install pyaudio
```

#### 3. ElevenLabs API Key Issues

```bash
# Check if API key is set
echo $ELEVENLABS_API_KEY

# Test ElevenLabs connection
python test_elevenlabs_simple.py
```

#### 4. Microphone Not Working

```bash
# Check available audio devices
arecord -l

# Test microphone
arecord -d 5 -f cd test.wav
aplay test.wav
```

#### 5. Permission Issues

```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Log out and log back in
```

## File Structure

```
SIH_MAITRI/
├── context_database.py          # Knowledge base
├── gemini_integration.py        # Gemini API integration
├── speech_maitri_no_ffmpeg.py   # Speech interface (recommended)
├── speech_maitri_fixed.py       # Speech interface (with FFmpeg)
├── interactive_test.py          # Text interface
├── demo.py                      # Demo scenarios
├── requirements.txt             # Python dependencies
└── UBUNTU_SETUP.md             # This guide
```

## API Keys Setup

### 1. Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key and set it as environment variable

### 2. ElevenLabs API Key

1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up for free account
3. Go to profile settings
4. Copy API key and set it as environment variable

## Testing the Setup

### 1. Test Basic Functionality

```bash
python demo.py
```

### 2. Test Speech Recognition

```bash
python interactive_test.py
# Choose option 1 for live conversation
```

### 3. Test Full Speech Interface

```bash
python speech_maitri_no_ffmpeg.py
# Choose option 2 for demo mode
```

## Development Notes

### Adding New Context

```python
from context_database import ContextDatabase

db = ContextDatabase()
db.add_custom_context(
    category="psychological",
    subcategory="new_topic",
    title="New Title",
    content="Your content here",
    keywords=["keyword1", "keyword2"],
    priority=3
)
```

### Customizing Voice

Edit `speech_maitri_no_ffmpeg.py` and change:

```python
self.voice_id = "EXAVITQu4vr4xnSDxMaL"  # Change to different voice ID
```

## Performance Tips

1. **Use virtual environment** to avoid conflicts
2. **Test with demo mode first** before live conversation
3. **Check microphone permissions** if speech recognition fails
4. **Use fallback TTS** if ElevenLabs has issues

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Test individual components (Gemini, ElevenLabs, speech recognition)
4. Check API key validity and permissions

## Next Steps

1. Test the basic functionality
2. Try the demo scenarios
3. Test speech-to-speech interface
4. Customize context database if needed
5. Integrate with your existing sentiment analysis code
