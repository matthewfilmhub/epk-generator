#!/bin/bash

# EPK Generator - Deployment Preparation Script
# This script prepares your files for deployment to Vercel

echo "🎬 EPK Generator - Deployment Preparation"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found"
    echo "   Please run this script from the project root directory"
    exit 1
fi

echo "✅ Found vercel.json"
echo ""

# Check required directories
echo "Checking project structure..."

if [ ! -d "api" ]; then
    echo "❌ Missing: api directory"
    exit 1
fi
echo "✅ api/ directory found"

if [ ! -d "frontend" ]; then
    echo "❌ Missing: frontend directory"
    exit 1
fi
echo "✅ frontend/ directory found"

if [ ! -f "api/main.py" ]; then
    echo "❌ Missing: api/main.py"
    exit 1
fi
echo "✅ api/main.py found"

if [ ! -f "api/epk_core.py" ]; then
    echo "❌ Missing: api/epk_core.py"
    exit 1
fi
echo "✅ api/epk_core.py found"

if [ ! -f "frontend/package.json" ]; then
    echo "❌ Missing: frontend/package.json"
    exit 1
fi
echo "✅ frontend/package.json found"

echo ""
echo "📋 Project Structure: OK"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# React
/frontend/build
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Vercel
.vercel

# EPK Projects (temporary files)
epk_projects/
/tmp/
*.zip
EOF
    echo "✅ .gitignore created"
else
    echo "✅ .gitignore exists"
fi

echo ""
echo "🔍 Pre-deployment Checklist:"
echo ""

# Check for sensitive information
echo "Checking for sensitive data..."
if grep -r "password\|secret\|api_key\|token" --include="*.py" --include="*.js" --include="*.jsx" . 2>/dev/null | grep -v "# " | grep -v "//" > /dev/null; then
    echo "⚠️  Warning: Found potential sensitive data in code"
    echo "   Please review before deploying"
else
    echo "✅ No obvious sensitive data found"
fi

echo ""
echo "📊 File Summary:"
echo "   Python files: $(find api -name "*.py" | wc -l)"
echo "   React files: $(find frontend/src -name "*.js" -o -name "*.jsx" 2>/dev/null | wc -l)"
echo "   Config files: $(ls *.json *.md 2>/dev/null | wc -l)"
echo ""

# Show git status
echo "📁 Git Status:"
if [ -d ".git" ]; then
    if git diff --quiet && git diff --cached --quiet; then
        echo "   ✅ No uncommitted changes"
    else
        echo "   ⚠️  You have uncommitted changes:"
        git status --short
    fi
else
    echo "   ⚠️  Git not initialized"
fi

echo ""
echo "🎯 Next Steps:"
echo ""
echo "1. Review the checklist above"
echo "2. If everything looks good:"
echo ""
echo "   git add ."
echo "   git commit -m 'Initial commit - EPK Generator'"
echo ""
echo "3. Create a GitHub repository at: https://github.com/new"
echo ""
echo "4. Push your code:"
echo ""
echo "   git remote add origin https://github.com/YOUR-USERNAME/epk-generator.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "5. Go to Vercel: https://vercel.com"
echo "   - Import your GitHub repository"
echo "   - Add environment variable: PLAYWRIGHT_BROWSERS_PATH=/tmp/.cache/ms-playwright"
echo "   - Deploy!"
echo ""
echo "📖 Detailed instructions: See DEPLOY_NOW.md"
echo "✅ Quick checklist: See CHECKLIST.md"
echo ""
echo "Good luck! 🚀"
