@echo off
REM EPK Generator - Deployment Preparation Script (Windows)
REM This script prepares your files for deployment to Vercel

echo.
echo 🎬 EPK Generator - Deployment Preparation
echo ==========================================
echo.

REM Check if we're in the right directory
if not exist "vercel.json" (
    echo ❌ Error: vercel.json not found
    echo    Please run this script from the project root directory
    exit /b 1
)

echo ✅ Found vercel.json
echo.

REM Check required directories
echo Checking project structure...

if not exist "api" (
    echo ❌ Missing: api directory
    exit /b 1
)
echo ✅ api\ directory found

if not exist "frontend" (
    echo ❌ Missing: frontend directory
    exit /b 1
)
echo ✅ frontend\ directory found

if not exist "api\main.py" (
    echo ❌ Missing: api\main.py
    exit /b 1
)
echo ✅ api\main.py found

if not exist "api\epk_core.py" (
    echo ❌ Missing: api\epk_core.py
    exit /b 1
)
echo ✅ api\epk_core.py found

if not exist "frontend\package.json" (
    echo ❌ Missing: frontend\package.json
    exit /b 1
)
echo ✅ frontend\package.json found

echo.
echo 📋 Project Structure: OK
echo.

REM Check if git is initialized
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
    echo ✅ Git initialized
) else (
    echo ✅ Git already initialized
)

REM Create .gitignore if it doesn't exist
if not exist ".gitignore" (
    echo 📝 Creating .gitignore...
    (
        echo # Python
        echo __pycache__/
        echo *.py[cod]
        echo *$py.class
        echo *.so
        echo .Python
        echo env/
        echo venv/
        echo ENV/
        echo *.egg-info/
        echo dist/
        echo build/
        echo.
        echo # Node
        echo node_modules/
        echo npm-debug.log*
        echo yarn-debug.log*
        echo yarn-error.log*
        echo.
        echo # React
        echo /frontend/build
        echo .DS_Store
        echo .env.local
        echo .env.development.local
        echo .env.test.local
        echo .env.production.local
        echo.
        echo # IDE
        echo .vscode/
        echo .idea/
        echo *.swp
        echo *.swo
        echo.
        echo # Vercel
        echo .vercel
        echo.
        echo # EPK Projects
        echo epk_projects/
        echo /tmp/
        echo *.zip
    ) > .gitignore
    echo ✅ .gitignore created
) else (
    echo ✅ .gitignore exists
)

echo.
echo 🔍 Pre-deployment Checklist:
echo.
echo ✅ Project structure verified
echo ✅ Git initialized
echo ✅ .gitignore created
echo.

echo 📁 Git Status:
if exist ".git" (
    git status --short
) else (
    echo    ⚠️  Git not initialized
)

echo.
echo 🎯 Next Steps:
echo.
echo 1. Review the checklist above
echo 2. If everything looks good:
echo.
echo    git add .
echo    git commit -m "Initial commit - EPK Generator"
echo.
echo 3. Create a GitHub repository at: https://github.com/new
echo.
echo 4. Push your code:
echo.
echo    git remote add origin https://github.com/YOUR-USERNAME/epk-generator.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 5. Go to Vercel: https://vercel.com
echo    - Import your GitHub repository
echo    - Add environment variable: PLAYWRIGHT_BROWSERS_PATH=/tmp/.cache/ms-playwright
echo    - Deploy!
echo.
echo 📖 Detailed instructions: See DEPLOY_NOW.md
echo ✅ Quick checklist: See CHECKLIST.md
echo.
echo Good luck! 🚀
echo.

pause
