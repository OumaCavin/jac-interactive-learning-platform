#!/bin/bash

# JAC Interactive Learning Platform - Fix Permission Issue and Create Migrations
# This script specifically fixes the file permissions inside Docker container

echo "=========================================="
echo "JAC Interactive Learning Platform"
echo "Fix Permission Issue & Create Migrations"
echo "=========================================="

cd ~/projects/jac-interactive-learning-platform

echo ""
echo "📥 Pulling latest changes..."
git pull origin main

echo ""
echo "🔧 Fixing permissions inside Docker container..."

# Fix permissions inside the container
docker-compose exec backend bash -c '
# Change to app directory
cd /app

# Check current user and file ownership
echo "Current user: $(whoami)"
echo "App directory owner: $(ls -la | grep apps | head -1)"

# Fix ownership of migrations directories to match container user
chown -R jac:jac apps/*/migrations/ 2>/dev/null || echo "chown may have failed"

# Fix permissions on migrations directories
chmod -R 755 apps/*/migrations/

# Fix permissions on existing migration files
find apps -path "*/migrations/*" -name "*.py" -exec chmod 644 {} \; 2>/dev/null || true

# Ensure __init__.py files exist and have correct permissions
find apps -path "*/migrations/" -name "__init__.py" -exec chmod 644 {} \; 2>/dev/null || true

echo "Permissions fixed"
'

echo ""
echo "🛠️ Creating migrations with fixed permissions..."
docker-compose exec backend python manage.py makemigrations collaboration gamification jac_execution learning --noinput

echo ""
echo "📊 Applying migrations to database..."
docker-compose exec backend python manage.py migrate

echo ""
echo "✅ Final migration status:"
docker-compose exec backend python manage.py showmigrations collaboration

echo ""
echo "🎉 MIGRATION PROCESS COMPLETED!"
echo "Check the output above for success messages."
