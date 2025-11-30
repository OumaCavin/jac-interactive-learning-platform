#!/bin/bash

echo "=== COMPREHENSIVE Django Admin Static Files Fix ==="
echo "Addressing missing static directories issue"
echo

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the jac-interactive-learning-platform directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

echo "✅ Found docker-compose.yml - proceeding with comprehensive fix..."

# Step 1: Check current static configuration
echo "🔍 Step 1: Checking current static files configuration..."
echo "Running diagnostic script..."
docker-compose exec backend python /app/check_static_config.py
echo

# Step 2: Create static root directory structure if missing
echo "🔄 Step 2: Ensuring static root directory exists..."
docker-compose exec backend mkdir -p /app/static
docker-compose exec backend mkdir -p /app/static/admin
docker-compose exec backend mkdir -p /app/static/admin/css

# Step 3: Run collectstatic with verbose output to see what's happening
echo "🔄 Step 3: Collecting static files with detailed output..."
docker-compose exec backend python manage.py collectstatic --verbosity=2 --noinput

# Step 4: Verify admin CSS files exist
echo "🔄 Step 4: Verifying admin CSS files..."
echo "Contents of /app/static/admin/css/:"
docker-compose exec backend ls -la /app/static/admin/css/ 2>/dev/null || echo "❌ CSS directory empty or missing"

echo "Contents of /app/static/admin/:"
docker-compose exec backend ls -la /app/static/admin/ 2>/dev/null || echo "❌ Admin directory missing"

# Step 5: Fix permissions
echo "🔄 Step 5: Fixing static file permissions..."
docker-compose exec backend chown -R jac:jac /app/static/

# Step 6: Restart backend container
echo "🔄 Step 6: Restarting backend container..."
docker-compose restart backend

# Wait for backend to fully start
echo "🔄 Step 7: Waiting for backend to start..."
sleep 10

# Test admin static files access
echo "🔄 Step 8: Testing admin static files access..."
echo "Testing dashboard.css..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/admin/css/dashboard.css)
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
    echo "This may indicate:"
    echo "- Static files not collected properly"
    echo "- Custom admin site configuration issues"
    echo "- URL routing problems"
    echo
    echo "🔍 Checking Docker logs for errors..."
    docker-compose logs --tail=10 backend
fi

echo
echo "=== Comprehensive Fix Complete ==="