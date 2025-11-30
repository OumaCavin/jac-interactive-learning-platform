#!/bin/bash

echo "=== FIX Custom Admin Static Files ==="
echo "Targeted fix for custom admin site CSS collection"
echo

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the jac-interactive-learning-platform directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

echo "✅ Found docker-compose.yml - proceeding with custom admin fix..."

# Step 1: Clear existing static files
echo "🔄 Step 1: Clearing existing static files..."
docker-compose exec backend rm -rf /var/www/static/admin/*
echo "✅ Cleared existing admin static files"

# Step 2: Force collectstatic with verbose output
echo "🔄 Step 2: Forcing Django admin static files collection..."
docker-compose exec backend python manage.py collectstatic --verbosity=2 --noinput --clear

# Step 3: Check if Django admin CSS files are now present
echo "🔄 Step 3: Checking Django admin CSS files..."
echo "Contents of /var/www/static/admin/css/:"
docker-compose exec backend ls -la /var/www/static/admin/css/ 2>/dev/null || echo "❌ Admin CSS directory still missing"

echo
echo "Checking for dashboard.css specifically:"
dashboard_exists=$(docker-compose exec backend ls /var/www/static/admin/css/dashboard.css 2>/dev/null && echo "YES" || echo "NO")
if [ "$dashboard_exists" = "YES" ]; then
    echo "✅ dashboard.css found!"
else
    echo "❌ dashboard.css still missing"
    echo
    echo "🔍 Checking what admin CSS files ARE available:"
    docker-compose exec backend find /var/www/static/admin -name "*.css" -type f 2>/dev/null || echo "No CSS files found"
fi

# Step 4: Fix permissions
echo "🔄 Step 4: Fixing static file permissions..."
docker-compose exec backend chown -R root:root /var/www/static/ 2>/dev/null || echo "Permission fix failed (normal in some Docker configs)"

# Step 5: Restart backend
echo "🔄 Step 5: Restarting backend container..."
docker-compose restart backend

# Wait for backend to fully start
echo "🔄 Step 6: Waiting for backend to start..."
sleep 10

# Test admin static files access
echo "🔄 Step 7: Testing admin static files access..."
echo "Testing dashboard.css..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/admin/css/dashboard.css 2>/dev/null)
echo "dashboard.css HTTP status: $response"

if [ "$response" = "200" ]; then
    echo "✅ SUCCESS: dashboard.css is now accessible!"
    echo "✅ Admin interface should now load properly with CSS styling"
    echo
    echo "🎯 Next steps:"
    echo "1. Clear your browser cache for localhost:8000"
    echo "2. Open an incognito window"
    echo "3. Visit http://localhost:8000/admin/"
    echo "4. Login with: admin / jac_admin_2024!"
    echo "5. The admin interface should now display with proper CSS styling"
else
    echo "❌ FAILED: dashboard.css still returns HTTP $response"
    echo
    echo "🔍 Final diagnostic - checking backend logs:"
    docker-compose logs --tail=5 backend
fi

echo
echo "=== Custom Admin Static Files Fix Complete ==="