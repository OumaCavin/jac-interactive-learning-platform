#!/bin/bash

# Quick Fix for Backend Health and Permissions
echo "🔧 Quick Fix: Backend Health and Migration Permissions"
echo "=================================================="

cd ~/projects/jac-interactive-learning-platform

echo ""
echo "📥 Pulling latest changes..."
git pull origin main

echo ""
echo "🔄 Restarting backend container to fix health issue..."
docker-compose restart backend
sleep 5

echo ""
echo "🔧 Fixing permissions inside container..."
docker-compose exec backend bash -c '
chown -R jac:jac /app/apps/*/migrations/ 2>/dev/null || true
chmod -R 755 /app/apps/*/migrations/
find /app/apps -name "*.py" -path "*/migrations/*" -exec chmod 644 {} \; 2>/dev/null || true
echo "Permissions fixed"
'

echo ""
echo "🛠️ Creating migrations..."
docker-compose exec backend python manage.py makemigrations collaboration gamification jac_execution learning --noinput

echo ""
echo "📊 Applying migrations..."
docker-compose exec backend python manage.py migrate

echo ""
echo "✅ Checking backend health..."
docker-compose ps backend

echo ""
echo "🎉 Done! Check migration status above."
