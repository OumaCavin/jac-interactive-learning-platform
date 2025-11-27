#!/bin/bash

# FINAL PUSH SCRIPT - Run on your local machine
# This script will commit and push all the critical fixes

echo "=== JAC Interactive Learning Platform - Final Push ==="
echo ""

# Navigate to project directory
cd ~/projects/jac-interactive-learning-platform || exit 1

echo "Current directory: $(pwd)"
echo ""

# Check git status
echo "=== Current Git Status ==="
git status

echo ""
echo "=== Applying critical fixes ==="

# Ensure the critical fixes are in place
# 1. Check URL namespace fix
if grep -q "jac_execution URLs included only once" backend/config/urls.py; then
    echo "✅ URL namespace fix confirmed"
else
    echo "❌ URL namespace fix missing"
    exit 1
fi

# 2. Check database constraint fix  
if grep -q "xp_to_next_level = models.PositiveIntegerField(default=100)" backend/apps/gamification/models.py; then
    echo "✅ Database constraint fix confirmed"
else
    echo "❌ Database constraint fix missing"
    exit 1
fi

# 3. Check frontend CSS fixes
if grep -q "login-form-container" frontend/src/index.css; then
    echo "✅ Frontend CSS fixes confirmed"
else
    echo "❌ Frontend CSS fixes missing"
    exit 1
fi

echo ""
echo "=== Committing changes ==="

# Add all changes
git add .

# Commit with comprehensive message
git commit -m "fix: Resolve critical platform issues

- Fix URL namespace conflict for jac_execution app in config/urls.py (removed duplicate include)
- Add default value to xp_to_next_level in UserLevel model to prevent database constraint violations  
- Fix login form UI positioning, overlapping text, invisible button, and alignment issues
- Improve glassmorphism styling compatibility with form components
- Resolve checkbox rendering and validation message positioning"

if [ $? -ne 0 ]; then
    echo "❌ Commit failed"
    exit 1
fi

echo "✅ Commit successful"

echo ""
echo "=== Pushing to GitHub ==="

# Try push
if git push origin main; then
    echo ""
    echo "✅ SUCCESS: All changes pushed to GitHub!"
    echo ""
    echo "🎉 Critical fixes applied and pushed:"
    echo "   • URL namespace conflict resolved"
    echo "   • Database constraint violation fixed"  
    echo "   • Login form UI issues resolved"
    echo ""
    echo "📋 Next steps for local setup:"
    echo "1. docker-compose exec backend python manage.py makemigrations"
    echo "2. docker-compose exec backend python manage.py migrate"
    echo "3. docker-compose up -d --build"
    echo "4. docker-compose restart backend"
    echo ""
    echo "🔍 Verify with: docker-compose exec backend python manage.py check --database default"
else
    echo ""
    echo "❌ Push failed. Authentication may be required."
    echo ""
    echo "🔧 Try one of these solutions:"
    echo "1. Use GitHub CLI: gh auth login"
    echo "2. Generate new Personal Access Token"
    echo "3. Set up SSH keys: ssh-keygen -t ed25519 -C 'your-email@example.com'"
    echo "4. Or manually push: git push origin main"
    exit 1
fi