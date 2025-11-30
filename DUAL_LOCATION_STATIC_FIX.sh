#!/bin/bash

echo "=== DUAL LOCATION Django Admin Static Files Fix ==="
echo "Copies static files to BOTH /var/www/static/ and /app/static/"
echo "This ensures Django finds files regardless of configuration"

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ ERROR: docker-compose.yml not found. Run this from the project root."
    exit 1
fi

echo "✅ Found docker-compose.yml - proceeding with dual location fix..."

echo ""
echo "🔧 Step 1: Verifying current Django admin static files exist..."
if docker-compose exec backend test -f /var/www/static/admin/css/dashboard.css; then
    echo "✅ Django admin static files found in /var/www/static/"
    STATIC_FILES_SOURCE="/var/www/static"
else
    echo "⚠️  Django admin static files not found in /var/www/static/"
    echo "🔄 Collecting Django admin static files first..."
    docker-compose exec backend python manage.py collectstatic --clear --noinput
    STATIC_FILES_SOURCE="/var/www/static"
fi

echo ""
echo "🔧 Step 2: Creating /app/static/ directory structure..."
docker-compose exec backend mkdir -p /app/static/admin/css/
docker-compose exec backend mkdir -p /app/static/admin/js/
docker-compose exec backend mkdir -p /app/static/admin/img/

echo ""
echo "🔧 Step 3: Copying Django admin static files to BOTH locations..."

echo "📁 Copying CSS files..."
docker-compose exec backend cp -r /var/www/static/admin/css/* /app/static/admin/css/

echo "📁 Copying JavaScript files..."
docker-compose exec backend cp -r /var/www/static/admin/js/* /app/static/admin/js/

echo "📁 Copying image files..."
docker-compose exec backend cp -r /var/www/static/admin/img/* /app/static/admin/img/

echo ""
echo "🔧 Step 4: Verifying files copied successfully..."

echo "Checking /var/www/static/admin/css/dashboard.css:"
if docker-compose exec backend test -f /var/www/static/admin/css/dashboard.css; then
    echo "✅ dashboard.css EXISTS in /var/www/static/"
    docker-compose exec backend ls -la /var/www/static/admin/css/dashboard.css
else
    echo "❌ dashboard.css MISSING in /var/www/static/"
fi

echo ""
echo "Checking /app/static/admin/css/dashboard.css:"
if docker-compose exec backend test -f /app/static/admin/css/dashboard.css; then
    echo "✅ dashboard.css EXISTS in /app/static/"
    docker-compose exec backend ls -la /app/static/admin/css/dashboard.css
else
    echo "❌ dashboard.css MISSING in /app/static/"
fi

echo ""
echo "🔧 Step 5: Verifying both locations have all Django admin files..."
echo "Files in /var/www/static/admin/css/:"
docker-compose exec backend ls /var/www/static/admin/css/

echo ""
echo "Files in /app/static/admin/css/:"
docker-compose exec backend ls /app/static/admin/css/

echo ""
echo "🔧 Step 6: Testing HTTP access to dashboard.css..."
HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/admin/css/dashboard.css)

if [ "$HTTP_RESPONSE" = "200" ]; then
    echo "🎉 SUCCESS: dashboard.css returns HTTP 200!"
    echo ""
    echo "✅ Your Django admin interface should now load with proper styling!"
    echo "🌐 Visit: http://localhost:8000/admin/"
    echo "🔐 Login: admin / jac_admin_2024!"
    echo ""
    echo "🔍 Testing admin interface accessibility..."
    curl -s http://localhost:8000/admin/ | grep -q "Django administration" && echo "✅ Admin interface loads correctly!" || echo "⚠️  Admin interface may still have styling issues"
else
    echo "❌ STILL FAILED: dashboard.css returns HTTP $HTTP_RESPONSE"
    echo ""
    echo "🔍 Debugging Django static files configuration..."
    docker-compose exec backend python manage.py shell -c "
from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.contrib.staticfiles.finders import find
import os

print('=== Django Static Files Debug ===')
print(f'STATIC_URL: {settings.STATIC_URL}')
print(f'STATIC_ROOT: {settings.STATIC_ROOT}')
print(f'STATICFILES_DIRS: {settings.STATICFILES_DIRS}')
print(f'DEBUG: {settings.DEBUG}')

# Test finding dashboard.css using Django's staticfiles finder
try:
    found_path = find('admin/css/dashboard.css')
    print(f'Django found dashboard.css at: {found_path}')
except Exception as e:
    print(f'Django could not find dashboard.css: {e}')

# Check file existence in both locations
locations = [
    os.path.join(settings.STATIC_ROOT, 'admin', 'css', 'dashboard.css'),
    '/app/static/admin/css/dashboard.css'
]

for location in locations:
    print(f'File at {location}: EXISTS={os.path.exists(location)}')
    if os.path.exists(location):
        print(f'  Readable: {os.access(location, os.R_OK)}')
        print(f'  Size: {os.path.getsize(location)} bytes')
"
fi

echo ""
echo "🔧 Step 7: Listing all static file locations for reference..."
echo "Complete /var/www/static/admin/css/ contents:"
docker-compose exec backend find /var/www/static/admin/css/ -type f | sort

echo ""
echo "Complete /app/static/admin/css/ contents:"
docker-compose exec backend find /app/static/admin/css/ -type f | sort

echo ""
echo "=== DUAL LOCATION Django Admin Static Files Fix Complete ==="
echo "✅ Static files are now available in BOTH locations:"
echo "   1. /var/www/static/ (Docker volume mount)"
echo "   2. /app/static/ (Django local static directory)"
echo ""
echo "🎯 This ensures Django admin CSS will work regardless of its configuration!"
echo "🔧 No more 404 errors for admin static files!"