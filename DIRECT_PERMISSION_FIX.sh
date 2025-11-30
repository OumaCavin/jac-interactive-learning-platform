#!/bin/bash

# Direct Permission Fix - Simple and Effective
echo "🔧 DIRECT PERMISSION FIX"
echo "========================"

cd ~/projects/jac-interactive-learning-platform

# Pull changes
git pull origin main

echo ""
echo "🔧 Running permission fix inside Docker container..."
docker-compose exec backend bash -c '
cd /app
echo "Fixing ownership..."
chown -R jac:jac apps/*/migrations/ 2>/dev/null
echo "Fixing permissions..."
chmod -R 755 apps/*/migrations/
find apps -path "*/migrations/*" -name "*.py" -exec chmod 644 {} \;
echo "Done!"
'

echo ""
echo "🛠️ Creating migrations..."
docker-compose exec backend python manage.py makemigrations collaboration gamification jac_execution learning --noinput

echo ""
echo "📊 Applying migrations..."
docker-compose exec backend python manage.py migrate

echo ""
echo "✅ SUCCESS! Check status above."
