@echo off
REM EPK Generator - Quick Setup Script (Windows)
REM This script sets up the development environment

echo.
echo 🎬 EPK Generator - Development Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9 or higher.
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16 or higher.
    exit /b 1
)

echo ✅ Node.js found
node --version
echo.

REM Setup Backend
echo 📦 Setting up Python backend...
cd api

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Install Playwright browsers
echo Installing Playwright browsers (this may take a few minutes)...
playwright install chromium

echo ✅ Backend setup complete!
echo.

REM Setup Frontend
echo 📦 Setting up React frontend...
cd ..\frontend

REM Install Node dependencies
echo Installing Node dependencies...
call npm install

echo ✅ Frontend setup complete!
echo.

REM Create sample environment file
cd ..
if not exist ".env" (
    echo Creating .env file...
    (
        echo # API Configuration
        echo API_PORT=8000
        echo API_HOST=0.0.0.0
        echo.
        echo # Frontend Configuration
        echo REACT_APP_API_URL=http://localhost:8000
        echo.
        echo # Playwright Configuration
        echo PLAYWRIGHT_BROWSERS_PATH=/tmp/.cache/ms-playwright
    ) > .env
    echo ✅ Environment file created
)

echo.
echo 🎉 Setup Complete!
echo.
echo To start development:
echo.
echo 1. Start the backend (in terminal 1):
echo    cd api
echo    venv\Scripts\activate
echo    python main.py
echo.
echo 2. Start the frontend (in terminal 2):
echo    cd frontend
echo    npm start
echo.
echo 3. Open your browser to: http://localhost:3000
echo.
echo For deployment instructions, see DEPLOYMENT.md
echo.

pause
