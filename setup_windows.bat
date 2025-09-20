@echo off
echo 🚀 MAITRI Windows Setup
echo =====================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install requirements
echo 📦 Installing requirements...
pip install -r requirements.txt

echo.
echo 🔑 Setting up Gemini API Key...
echo Please enter your Gemini API key:
set /p GEMINI_API_KEY=

if "%GEMINI_API_KEY%"=="" (
    echo ❌ No API key entered. Please run the script again.
    pause
    exit /b 1
)

REM Set environment variable for current session
set GEMINI_API_KEY=%GEMINI_API_KEY%

REM Set permanently
setx GEMINI_API_KEY "%GEMINI_API_KEY%"

echo.
echo ✅ API key set successfully!
echo 🎉 Setup complete! You can now run: python demo.py
pause

