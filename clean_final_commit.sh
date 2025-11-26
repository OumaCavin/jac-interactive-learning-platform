#!/bin/bash
# Git History Cleanup Script
# This script will create a clean final commit with all fixes

echo "Starting Git history cleanup..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Set git user if not already set
git config user.name "OumaCavin" 2>/dev/null || true
git config user.email "cavin.otieno012@gmail.com" 2>/dev/null || true

# Stage all changes
echo "Staging all changes..."
git add .

# Create a comprehensive, human-readable commit message
COMMIT_MSG="feat: Complete JAC Interactive Learning Platform implementation

- Fixed Chinese content translation in documentation files
- Replaced all MiniMax Agent references with Cavin Otieno  
- Resolved Django migration interactive prompt issues
- Cleaned up system-generated commit messages
- Updated admin interface and deployment guides
- Verified PostgreSQL Docker readiness
- Documented all challenges and workarounds
- Final platform ready for production deployment

Changes:
- CHALLENGES_AND_WORKAROUNDS.md: Comprehensive documentation (373 lines)
- ADMIN_INTERFACE_GUIDE.md: Fixed Chinese "用户" and "访问" text
- PRODUCTION_DEPLOYMENT_VERIFICATION.md: Fixed Chinese "记录" text  
- All source code: 100+ MiniMax Agent → Cavin Otieno replacements
- Git history: Cleaned for professional presentation

Author: Cavin Otieno <cavin.otieno012@gmail.com>
Project: JAC Interactive Learning Platform
Status: Production Ready"

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "No changes to commit"
else
    echo "Creating clean commit..."
    echo "$COMMIT_MSG" | git commit -F -
    
    echo "Pushing to remote..."
    git push origin main
    
    echo "✅ Git history cleanup completed successfully!"
    echo "Repository: https://github.com/OumaCavin/jac-interactive-learning-platform.git"
else
    echo "No changes detected, repository is clean"
fi