#!/bin/bash
# Commit and push all fixes

cd /workspace

echo "🔧 Committing and pushing all fixes..."

# Add all changes
git add .

# Check status
echo "📋 Git status:"
git status --short

# Commit
git commit -m "Fix: Enhanced migration automation and URL namespace resolution

- Fixed duplicate agents URL namespace in backend/config/urls.py
- Enhanced quick_fix_now.sh with explicit app targeting (users, learning)
- Added field verification and dry-run checks for migrations
- Created comprehensive migration fix script
- All migration issues will be resolved automatically"

# Push to remote
echo "🚀 Pushing to remote..."
git push origin main

echo "✅ All fixes committed and pushed!"