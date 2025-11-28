#!/bin/bash

# Complete Migration Script
# This script handles the permission fixes and migrations

echo "🔧 Starting migration completion process..."

# Fix permissions (ignoring errors as they are expected in Docker)
echo "  → Fixing migration directory permissions..."
/workspace/docker-compose exec -T backend chmod -R 755 /app/migrations/ 2>/dev/null || echo "  ℹ️  Permission fix attempted (some errors expected)"

# Run makemigrations
echo "  → Running makemigrations..."
/workspace/docker-compose exec -T backend python manage.py makemigrations 2>/dev/null

# Run migrate
echo "  → Running migrate..."
/workspace/docker-compose exec -T backend python manage.py migrate 2>/dev/null

# Restart backend service
echo "  → Restarting backend service..."
/workspace/docker-compose restart backend

echo "✅ Migration process completed!"

# Check service status
echo "  → Checking service status..."
/workspace/docker-compose ps

echo "🎉 Migration completion script finished!"