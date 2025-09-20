#!/bin/bash

# MAITRI Ubuntu Setup Script
# This script sets up MAITRI on Ubuntu Linux

echo "🚀 MAITRI Ubuntu Setup"
echo "======================"

# Check if running on Ubuntu/Debian
if ! command -v apt &> /dev/null; then
    echo "❌ This script is designed for Ubuntu/Debian systems"
    echo "Please install dependencies manually using your package manager"
    exit 1
fi

# Update package list
echo "📦 Updating package list..."
sudo apt update

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y ffmpeg
sudo apt install -y portaudio19-dev
sudo apt install -y espeak espeak-data
sudo apt install -y git

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv maitri_env

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source maitri_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Handle PyAudio installation (common issue on Linux)
if ! python -c "import pyaudio" 2>/dev/null; then
    echo "🔧 Installing PyAudio (this might take a moment)..."
    pip install pyaudio
fi

# Test installations
echo "🧪 Testing installations..."

# Test Python packages
python -c "import google.generativeai; print('✅ Google Generative AI')" || echo "❌ Google Generative AI failed"
python -c "import speech_recognition; print('✅ Speech Recognition')" || echo "❌ Speech Recognition failed"
python -c "import pyttsx3; print('✅ PyTTSx3')" || echo "❌ PyTTSx3 failed"
python -c "import elevenlabs; print('✅ ElevenLabs')" || echo "❌ ElevenLabs failed"

# Test FFmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg installed"
else
    echo "❌ FFmpeg not found"
fi

# Test audio system
if command -v arecord &> /dev/null; then
    echo "✅ Audio system available"
else
    echo "❌ Audio system not available"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set your API keys:"
echo "   export GEMINI_API_KEY='your_gemini_key'"
echo "   export ELEVENLABS_API_KEY='your_elevenlabs_key'"
echo ""
echo "2. Activate virtual environment:"
echo "   source maitri_env/bin/activate"
echo ""
echo "3. Test the system:"
echo "   python demo.py"
echo "   python speech_maitri_no_ffmpeg.py"
echo ""
echo "For detailed instructions, see UBUNTU_SETUP.md"
