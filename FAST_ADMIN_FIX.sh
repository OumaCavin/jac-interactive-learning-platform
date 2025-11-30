#!/bin/bash

echo "🚀 Fast Admin Static Fix"
echo "========================"

cd ~/projects/jac-interactive-learning-platform

# Step 1: Collect static files
echo "📦 Collecting static files..."
docker-compose exec backend python manage.py collectstatic --noinput --clear

# Step 2: Fix permissions
echo "🔧 Fixing permissions..."
docker-compose exec backend bash -c "
chown -R jac:jac /app/staticfiles/ 2>/dev/null
chmod -R 755 /app/staticfiles/ 2>/dev/null
echo 'Permissions fixed'
"

# Step 3: Restart backend
echo "🔄 Restarting backend..."
docker-compose restart backend

# Step 4: Wait and test
echo "⏳ Waiting for backend to start..."
sleep 8

echo "🧪 Testing admin CSS..."
curl -I http://localhost:8000/static/admin/css/dashboard.css

echo ""
echo "✅ Static fix complete!"
echo "🌐 Now try: http://localhost:8000/admin/"
echo "👤 Login: admin / jac_admin_2024!"