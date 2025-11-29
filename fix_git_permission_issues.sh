#!/bin/bash

# Script to fix Git permission issues and apply UI fixes

echo "🔧 Fixing Git permission issues and applying UI fixes..."

# 1. Stop all Docker containers
echo "📦 Stopping Docker containers..."
docker-compose down

# 2. Fix file permissions in backend templates
echo "🔐 Fixing file permissions..."
sudo chown -R $USER:$USER backend/templates/admin/
sudo chmod -R 755 backend/templates/admin/

# 3. Clean up any git conflicts
echo "🧹 Cleaning up Git conflicts..."
git reset --hard origin/main

# 4. Start containers again
echo "🚀 Starting Docker containers..."
docker-compose up -d

# 5. Verify containers are running
echo "✅ Verifying containers..."
docker-compose ps

echo "✨ Done! UI fixes should now be applied."