#!/bin/bash

# YOLO11 API Startup Script
# This script helps setup and run the YOLO11 API backend

echo "🚀 YOLO11 API Setup Script"
echo "=========================="

# Create required directories
echo "📁 Creating directories..."
mkdir -p models logs temp

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Check if model exists
if [ ! -f "models/best.pt" ]; then
    echo "⚠️  Custom model not found at models/best.pt"
    echo "   The API will use YOLO11n as fallback"
    echo "   To use your custom model, place it at models/best.pt"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "   Please review and update .env file as needed"
fi

echo "✅ Setup complete!"
echo ""
echo "🏃 Starting the API server..."
echo "   API will be available at: http://localhost:8000"
echo "   Documentation at: http://localhost:8000/docs"
echo ""

# Start the server
python main.py