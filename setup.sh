#!/bin/bash

echo "=================================="
echo "AI Honeypot Setup Script"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p logs configs analysis/output

# Check for Docker
echo ""
if command -v docker &> /dev/null; then
    echo "✅ Docker found: $(docker --version)"
    echo "You can use: docker-compose up -d"
else
    echo "⚠️  Docker not found. You'll need to run components manually."
fi

# Check for Ollama
echo ""
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found: $(ollama --version)"
    echo "Pulling recommended model..."
    ollama pull llama3.2:3b
else
    echo "⚠️  Ollama not found. AI honeypot will use fallback mode or requires OpenAI API key."
    echo "Install from: https://ollama.com"
fi

echo ""
echo "=================================="
echo "Setup Complete! 🎉"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Start AI honeypot:         python ai-honeypot/ai_honeypot.py"
echo "2. Start traditional honeypot: python traditional-honeypot/traditional_honeypot.py"
echo "3. Start traffic generator:    python traffic-gen/traffic_generator.py"
echo "4. Test connection:            ssh user@localhost -p 2222"
echo "5. Run analysis:               python analysis/analyzer.py"
echo ""
echo "Or use Docker:"
echo "  docker-compose up -d"
echo ""
echo "For OpenAI API:"
echo "  export OPENAI_API_KEY='your-key-here'"
echo ""
echo "Read README.md for full instructions!"
