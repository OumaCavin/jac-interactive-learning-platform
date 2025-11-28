#!/bin/bash

# Manual Git Commands for Commit and Push
# Copy and paste these commands in your local terminal

echo "=== Step-by-step Git Commands ==="
echo ""

# Navigate to your project
echo "cd ~/projects/jac-interactive-learning-platform"
echo ""

# Check current status
echo "# Check current git status"
echo "git status"
echo ""

# Pull latest changes
echo "# Pull latest changes from GitHub"
echo "git pull origin main"
echo ""

# Add all changes
echo "# Stage all changes"
echo "git add ."
echo ""

# Commit with detailed message
echo "# Commit the fixes"
echo 'git commit -m "fix: Resolve critical platform issues
- Fix URL namespace conflict for jac_execution app in config/urls.py  
- Add default value to xp_to_next_level in UserLevel model to prevent database constraint violations
- Fix login form UI positioning, overlapping text, invisible button, and alignment issues
- Improve glassmorphism styling compatibility with form components
- Resolve checkbox rendering and validation message positioning"'
echo ""

# Push to GitHub
echo "# Push to GitHub repository"
echo "git push origin main"
echo ""

echo "=== Authentication Notes ==="
echo "If you get authentication errors, you may need to:"
echo "1. Use GitHub CLI: gh auth login"
echo "2. Set up SSH keys: ssh-keygen -t ed25519 -C 'your-email@example.com'"
echo "3. Add SSH key to GitHub account"
echo "4. Or reconfigure remote with token: git remote set-url origin https://[TOKEN]@github.com/[USERNAME]/[REPO].git"
echo ""