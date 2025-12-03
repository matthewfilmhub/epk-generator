#!/bin/bash

# Git Push Diagnostic Script
# Run this to see what's wrong with your git push

echo "========================================="
echo "GIT PUSH DIAGNOSTIC"
echo "========================================="
echo ""

echo "📁 Current Directory:"
pwd
echo ""

echo "📋 Git Status:"
git status
echo ""

echo "🔗 Git Remotes:"
git remote -v
echo ""

echo "🌿 Git Branches:"
git branch -a
echo ""

echo "📝 Recent Commits (last 3):"
git log --oneline -3 2>/dev/null || echo "No commits yet"
echo ""

echo "👤 Git User Config:"
echo "Name: $(git config user.name)"
echo "Email: $(git config user.email)"
echo ""

echo "🔍 Checking GitHub Connection..."
if git ls-remote origin HEAD &>/dev/null; then
    echo "✅ Connected to GitHub repository"
else
    echo "❌ Cannot connect to GitHub repository"
    echo "   Check your remote URL and credentials"
fi
echo ""

echo "========================================="
echo "COMMON SOLUTIONS:"
echo "========================================="
echo ""
echo "1. Authentication Issues:"
echo "   git config --global credential.helper store"
echo "   git push (enter GitHub token as password)"
echo ""
echo "2. No Remote Set:"
echo "   git remote add origin https://github.com/YOUR-USERNAME/epk-generator.git"
echo ""
echo "3. Wrong Branch:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Nothing to Commit:"
echo "   git add ."
echo "   git commit -m 'Update files'"
echo "   git push"
echo ""

echo "📖 Full guide: GIT_PUSH_TROUBLESHOOTING.md"
echo ""
