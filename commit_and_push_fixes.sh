#!/bin/bash

# Commit and Push All Platform Fixes
# Run this script in your local project directory

echo "=== JAC Interactive Learning Platform - Commit and Push Fixes ==="
echo ""

# Navigate to project directory (adjust path if different)
PROJECT_DIR="$HOME/projects/jac-interactive-learning-platform"
if [ ! -d "$PROJECT_DIR" ]; then
    PROJECT_DIR="./jac-interactive-learning-platform"
fi

cd "$PROJECT_DIR" || exit 1

echo "Working directory: $(pwd)"
echo ""

# Check if git repository
if [ ! -d ".git" ]; then
    echo "Error: Not a git repository. Please run this from your project directory."
    exit 1
fi

# Show current git status
echo "=== Current Git Status ==="
git status
echo ""

# Pull latest changes first
echo "=== Pulling latest changes from origin/main ==="
git pull origin main

# Add all changes
echo ""
echo "=== Adding all changes ==="
git add .

# Commit with comprehensive message
echo ""
echo "=== Committing changes ==="
git commit -m "fix: Resolve critical platform issues

- Fix URL namespace conflict for jac_execution app in config/urls.py
- Add default value to xp_to_next_level in UserLevel model to prevent database constraint violations
- Fix login form UI positioning, overlapping text, invisible button, and alignment issues
- Improve glassmorphism styling compatibility with form components
- Resolve checkbox rendering and validation message positioning"

echo ""
echo "=== Pushing to origin/main ==="
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully committed and pushed all fixes!"
    echo ""
    echo "Next steps to apply fixes:"
    echo "1. docker-compose exec backend python manage.py makemigrations"
    echo "2. docker-compose exec backend python manage.py migrate"
    echo "3. docker-compose up -d --build"
    echo "4. docker-compose restart backend"
    echo ""
    echo "To verify: docker-compose exec backend python manage.py check --database default"
else
    echo ""
    echo "❌ Push failed. You may need to:"
    echo "- Set up SSH keys for GitHub"
    echo "- Or use GitHub CLI: gh auth login"
    echo "- Or manually push: git push origin main"
    exit 1
fi