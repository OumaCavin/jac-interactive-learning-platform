#!/bin/bash

echo "=== Django Admin Static Files Fix ==="
echo "This script will fix the admin interface CSS issues"
echo

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the jac-interactive-learning-platform directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

echo "✅ Found docker-compose.yml - proceeding with fix..."

# Step 1: Collect static files
echo "🔄 Step 1: Collecting static files..."
docker-compose exec backend python manage.py collectstatic --noinput

# Step 2: Fix static file permissions
echo "🔄 Step 2: Fixing static file permissions..."
docker-compose exec backend chown -R jac:jac /app/static/

# Step 3: Restart backend container
echo "🔄 Step 3: Restarting backend container..."
docker-compose restart backend

# Wait for backend to fully start
echo "🔄 Step 4: Waiting for backend to start..."
sleep 5

# Test admin access
echo "🔄 Step 5: Testing admin static files access..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/admin/css/dashboard.css)

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
    echo "Please check the Docker logs:"
    echo "docker-compose logs --tail=20 backend"
fi

echo
echo "=== Fix Complete ==="