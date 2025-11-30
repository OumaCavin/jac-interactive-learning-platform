#!/bin/bash

# JAC Interactive Learning Platform - Fix Permissions and Create Migrations
# This script fixes the permission issue and creates migrations

echo "=========================================="
echo "JAC Interactive Learning Platform"
echo "Fix Permissions and Create Migrations"
echo "=========================================="

# Navigate to project directory
cd ~/projects/jac-interactive-learning-platform

# Pull latest changes
echo ""
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Wait for git to complete
sleep 3

# Check backend container status
echo ""
echo "🔍 Checking backend container status..."
docker-compose ps backend

echo ""
echo "🐛 Checking backend logs for issues..."
docker-compose logs --tail=10 backend

echo ""
echo "🔧 Fixing permissions in migrations directories..."
# Fix permissions inside Docker container
docker-compose exec backend bash -c 'chown -R jac:jac /app/apps/*/migrations/ 2>/dev/null || echo "chown failed, trying chmod..."'
docker-compose exec backend bash -c 'chmod -R 755 /app/apps/*/migrations/ || echo "chmod failed"'
docker-compose exec backend bash -c 'find /app/apps -name "*.py" -path "*/migrations/*" -exec chmod 644 {} \; || echo "find chmod failed"'

echo ""
echo "🛠️ Creating migrations for collaboration, gamification, jac_execution, learning..."
docker-compose exec backend python manage.py makemigrations collaboration gamification jac_execution learning --noinput

echo ""
echo "📊 Applying migrations to database..."
docker-compose exec backend python manage.py migrate

echo ""
echo "✅ Migration status:"
docker-compose exec backend python manage.py showmigrations

echo ""
echo "🎉 Migrations completed successfully!"
echo "Your JAC Interactive Learning Platform database schema is now up-to-date."
