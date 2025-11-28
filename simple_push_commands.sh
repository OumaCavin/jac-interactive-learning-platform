#!/bin/bash

# Simple Push Commands - Copy and paste these in your local terminal

cd ~/projects/jac-interactive-learning-platform

# Verify fixes are in place
echo "Checking critical fixes..."
grep -q "jac_execution URLs included only once" backend/config/urls.py && echo "✅ URL fix confirmed" || echo "❌ URL fix missing"
grep -q "xp_to_next_level = models.PositiveIntegerField(default=100)" backend/apps/gamification/models.py && echo "✅ Database fix confirmed" || echo "❌ Database fix missing"  
grep -q "login-form-container" frontend/src/index.css && echo "✅ Frontend fix confirmed" || echo "❌ Frontend fix missing"

# Commit and push
echo ""
echo "Committing and pushing..."
git add .
git commit -m "fix: Resolve critical platform issues

- Fix URL namespace conflict for jac_execution app in config/urls.py (removed duplicate include)
- Add default value to xp_to_next_level in UserLevel model to prevent database constraint violations  
- Fix login form UI positioning, overlapping text, invisible button, and alignment issues
- Improve glassmorphism styling compatibility with form components
- Resolve checkbox rendering and validation message positioning"
git push origin main