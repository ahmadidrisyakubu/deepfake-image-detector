#!/bin/bash

# Quick start script for local development

echo "🚀 Starting Deepfake Detector..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

# Run the application
echo ""
echo "✅ Starting Flask application..."
echo "🌐 Open your browser and navigate to: http://localhost:5000"
echo ""
python app.py
