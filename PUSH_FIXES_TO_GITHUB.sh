#!/bin/bash

# Script to push the Dockerfile fixes to GitHub
# Author: Cavin Otieno

echo "🚀 Pushing Dockerfile fixes to GitHub..."
echo

# Check if we're in the right directory
if [ ! -f "backend/Dockerfile" ]; then
    echo "❌ Error: backend/Dockerfile not found. Make sure you're in the project root directory."
    exit 1
fi

# Check git status
echo "📊 Current git status:"
git status --short
echo

# Pull latest changes first
echo "📥 Pulling latest changes from remote..."
git pull origin main

# Check if there are any local changes to commit
if git diff --quiet; then
    echo "✅ No changes to commit"
else
    echo "📝 Committing changes..."
    git add backend/Dockerfile
    git commit -m "fix(dockerfile): remove invalid syntax and simplify virtual environment handling

- Remove invalid || operator from COPY command
- Simplify venv copying to use consistent /home/jac/venv location  
- Update PATH variables to use single venv location
- Remove fallback logic from entrypoint script
- Resolve Docker build syntax errors"
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed Dockerfile fixes to GitHub!"
    echo
    echo "🎯 You can now test the Docker build:"
    echo "   docker-compose build --no-cache backend"
    echo "   docker-compose up -d"
else
    echo "❌ Push failed. Please check your GitHub credentials."
    echo
    echo "💡 Alternative: Run these commands locally:"
    echo "   git add backend/Dockerfile"
    echo "   git commit -m 'fix(dockerfile): remove invalid syntax and simplify virtual environment handling'"
    echo "   git push origin main"
fi