#!/bin/bash
# Quick fix for your current permission issue

echo "🔧 Fixing your current permission issue..."

# Fix permissions on migration directories
docker-compose exec backend chmod -R 755 /app/
docker-compose exec backend chmod -R 755 /app/migrations/
docker-compose exec backend find /app -type d -name migrations -exec chmod -R 755 {} \;

echo "✅ Permissions fixed! Now try the migration again..."
echo ""
echo "Run this command:"
echo "docker-compose exec backend python manage.py makemigrations --noinput"