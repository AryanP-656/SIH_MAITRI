# MAITRI Windows Setup Script
# Run this script to set up your environment

Write-Host "🚀 MAITRI Windows Setup" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host "📦 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Set up environment variable
Write-Host "🔑 Setting up Gemini API Key..." -ForegroundColor Yellow
$apiKey = Read-Host "Enter your Gemini API key"

if ($apiKey -and $apiKey -ne "your_api_key_here") {
    # Set for current session
    $env:GEMINI_API_KEY = $apiKey
    
    # Set permanently for user
    [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", $apiKey, "User")
    
    Write-Host "✅ API key set successfully!" -ForegroundColor Green
    Write-Host "   - Current session: Set" -ForegroundColor Green
    Write-Host "   - Permanent: Set" -ForegroundColor Green
} else {
    Write-Host "❌ Invalid API key. Please run the script again with a valid key." -ForegroundColor Red
    exit 1
}

# Test the setup
Write-Host "🧪 Testing setup..." -ForegroundColor Yellow
python -c "import os; print('✅ Environment variable set:', 'GEMINI_API_KEY' in os.environ)"

Write-Host "🎉 Setup complete! You can now run: python demo.py" -ForegroundColor Green

