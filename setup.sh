#!/bin/bash

# EPK Generator - Quick Setup Script
# This script sets up the development environment

set -e  # Exit on error

echo "🎬 EPK Generator - Development Setup"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python $(python3 --version) found"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Node.js $(node --version) found"
echo ""

# Setup Backend
echo "📦 Setting up Python backend..."
cd api

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers (this may take a few minutes)..."
playwright install chromium

echo "✅ Backend setup complete!"
echo ""

# Setup Frontend
echo "📦 Setting up React frontend..."
cd ../frontend

# Install Node dependencies
echo "Installing Node dependencies..."
npm install

echo "✅ Frontend setup complete!"
echo ""

# Create sample environment file
cd ..
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# API Configuration
API_PORT=8000
API_HOST=0.0.0.0

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000

# Playwright Configuration
PLAYWRIGHT_BROWSERS_PATH=/tmp/.cache/ms-playwright
EOF
    echo "✅ Environment file created"
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "To start development:"
echo ""
echo "1. Start the backend (in terminal 1):"
echo "   cd api"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   python main.py"
echo ""
echo "2. Start the frontend (in terminal 2):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Open your browser to: http://localhost:3000"
echo ""
echo "For deployment instructions, see DEPLOYMENT.md"
echo ""
